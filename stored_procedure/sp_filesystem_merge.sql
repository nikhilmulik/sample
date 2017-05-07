SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[cdm_sp_filesystem_merge](
	@md5 nchar(32),
	@sha256 nchar(64),
	@users_id TINYINT,
	@noRepeat TINYINT = NULL,  --Used by SP when it calls itself to prevent possibility of 
							   --infinite loop if something goes wrong (e.g. a delete/update fails)
	@filesystem_id bigint = NULL OUTPUT,
	@printRes TINYINT = 0
)
AS

BEGIN
	SET NOCOUNT ON

     --Check required fields
	IF @md5 IS NULL
		BEGIN
			RAISERROR ('md5 is a required parameter.',16,1)
			RETURN -100
		END

	IF @sha256 IS NULL
		BEGIN
			RAISERROR ('sha256 is a required parameter.',16,1)
			RETURN -100
		END

	IF @users_id IS NULL
		BEGIN
			RAISERROR ('users_id is a required parameter.',16,1)
			RETURN -100
		END
		
		
	DECLARE @rowCount INT	
	DECLARE @ErrorMessage NVARCHAR(max), @ErrorSeverity INT, @ErrorState INT	
		
    SELECT @rowCount = COUNT(id) FROM filesystem WHERE [MD5] = @md5 OR SHA256=@sha256
    --Possible cases are:
    --MD5 & SHA256 (Both Non NULL)
    --MD5 & NULL SHA256
    --SHA256 & NULL MD5 
    --MD5 with different SHA256
    --SHA256 with different MD5
    --Both of these last cases are not handled by this sproc since it wouldn't know which pairing is correct.
    IF (@rowCount>1)
    BEGIN

		DECLARE @keepFilesystemId BIGINT,    
		        @removeFilesystemId BIGINT, 
		        @idBoth BIGINT,
		        @idMD5 BIGINT,
		        @idSHA256 BIGINT,
		        @reason NVARCHAR(440),
		        @reason_id INT,
		        @actionType_id TINYINT
		
		SET @reason = 'Filesystem rows relating to the same file merged.'
		SET @actionType_id = 11 --Action type id relating to a merge action.
    
		--Determine if a row with both the MD5 & SHA256 exists (if so this is the row to merge into)
		SELECT @idBoth = id FROM filesystem WHERE [MD5] = @md5 AND SHA256=@sha256
		SELECT @idMD5 = id FROM filesystem WHERE [MD5] = @md5 AND SHA256 IS NULL
		SELECT @idSHA256 = id FROM filesystem WHERE [MD5] IS NULL AND SHA256 =@sha256


		--Pick 2 filesystem ids to merge (possible to have up to 3 options)
		--Ideally want to keep the row that has both the MD5 and SHA256 (if it exists).
		SELECT @keepFilesystemId = CASE 
			WHEN @idBoth IS NOT NULL THEN @idBoth
			WHEN @idBoth IS NULL AND @idMD5 IS NOT NULL Then @idMD5
			WHEN @idBoth IS NULL AND @idMD5 IS NULL Then NULL
        END

		--Pick the second filesystem id - row that will be deleted.
		SELECT @removeFilesystemId = CASE 
			WHEN @idBoth IS NOT NULL AND @idMD5 IS NOT NULL THEN @idMD5
			WHEN @idBoth IS NULL AND @idSHA256 IS NOT NULL THEN @idSHA256
			WHEN (@idBoth IS NULL OR @idMD5 IS NULL) AND @idSHA256 IS NOT NULL THEN @idSHA256
			WHEN (@idBoth IS NULL OR @idMD5 IS NULL) AND @idSHA256 IS NULL THEN NULL
        END

		/*If we don't have 2 filesystem rows to merge then no further action needed.
		Do not return any value - this way the caller knows no merge took place
		& can log an error/take action if a merge was expected.*/
		IF (@keepFilesystemId IS NULL OR @removeFilesystemId IS NULL)
			RETURN					
		
		DECLARE --Variables for dhf, softwareversion_has_filesystem, relating to filesystem row 
				--that will be dropped
				@removeDhfId BIGINT,
				@removeContributor_id SMALLINT,
				@removeContributorData_id BIGINT,
				@removeSoftwareVersion_id INT,
				@removePathRedo_id BIGINT,
				@removeDataset_id TINYINT,
				@removePathDS_id BIGINT,
				@removeSourceDhf NVARCHAR(255),
				--Variables relating to filesystem row that will be kept
				@keepDhfId BIGINT,
				@keepPathDS_id BIGINT,
				@keepSourceDhf NVARCHAR(255)

		--Variables relating to the filesystem row that will be removed
		DECLARE	@removeSize BIGINT, 
				@removeSHA NCHAR(40),
				@removeSHA224 NCHAR(56),
				@removeSHA384 NCHAR(96),
				@removeSHA512 NCHAR(128),
				@removeTroj1 NVARCHAR(8),
				@removeTroj2 NVARCHAR(8),
				@removeTroj4 NVARCHAR(8),
				@removeAttribute SMALLINT,			
				@removeArchitecture_id TINYINT,
				@removeSource NVARCHAR(255),
				@removeTrust_id TINYINT,
				@removeFull_info TINYINT,
				@removeSignature_id BIGINT,
				@removeGcrcData_id BIGINT,
				@removeGvmCRCData_id BIGINT,			
				@removeMime_id INT,
				@removeMagic_id INT,
				@removePeVersionInfo_id INT,
				@removeMicroMalHeur_id INT,
				@removeCatHash_id INT,
				@removeSmartHash_id INT
			
		SELECT
		  @removeSize = [size]
		 ,@removeSHA = [SHA]
		 ,@removeSHA224 = [SHA224]
		 ,@removeSHA384 = [SHA384]
		 ,@removeSHA512 = [SHA512]
		 ,@removeTroj1 = [troj1]
		 ,@removeTroj2 = [troj2]
		 ,@removeTroj4 = [troj4]
		 ,@removeMicroMalHeur_id = [microMalHeur_id]
		 ,@removeCatHash_id = [catHash_id]
		 ,@removeSmartHash_id = [smartHash_id]
		 ,@removeAttribute = [attribute]
		 ,@removeMime_id = [mime_id]
		 ,@removeMagic_id = [magic_id]
		 ,@removeArchitecture_id = [architecture_id]
		 ,@removePeVersionInfo_id = [peVersionInfo_id]
		 ,@removeSource = [source]
		 ,@removeTrust_id = [trust_id]
		 ,@removeFull_info = [full_info]
		 ,@removeSignature_id = [signature_id]
		 ,@removeGcrcData_id = [gcrcData_id]
		 ,@removeGvmCRCData_id = [gvmCRCData_id]
		FROM [dbo].[filesystem] WHERE [id] = @removeFilesystemId

		--Update the filesystem row that will be keep with any data missing which is present in the row to remove
		UPDATE [dbo].[filesystem]
		SET [size] = ISNULL(size, @removeSize)
			  ,[MD5] = ISNULL(md5, @md5)
			  ,[SHA] = ISNULL(sha, @removeSHA)
			  ,[SHA224] = ISNULL(sha224, @removeSHA224)
			  ,[SHA256] = ISNULL(sha256, @sha256)
			  ,[SHA384] = ISNULL(sha384, @removeSHA384)
			  ,[SHA512] = ISNULL(sha512, @removeSHA512)
			  ,[troj1] = ISNULL(troj1, @removeTroj1)
			  ,[troj2] = ISNULL(troj2, @removeTroj2)
			  ,[troj4] = ISNULL(troj4, @removeTroj4)
			  ,[attribute] = ISNULL(attribute, @removeAttribute)
			  ,[mime_id] = ISNULL(mime_id, @removeMime_id)
			  ,[magic_id] = ISNULL(magic_id, @removeMagic_id)
			  ,[architecture_id] = ISNULL(architecture_id, @removeArchitecture_id)
			  ,[peVersionInfo_id] = ISNULL(peVersionInfo_id, @removePeVersionInfo_id)
			  ,[source] = ISNULL([source], @removeSource)
			  ,[trust_id] = ISNULL(trust_id, @removeTrust_id)
			  ,[full_info] = ISNULL(full_info, @removeFull_info)
			  ,[signature_id] = ISNULL(signature_id, @removeSignature_id)
			  ,[gcrcData_id] = ISNULL(gcrcData_id, @removeGcrcData_id)
			  ,[gvmCRCData_id] = ISNULL(gvmCRCData_id, @removeGvmCRCData_id)
			  ,[microMalHeur_id] = ISNULL(microMalHeur_id, @removeMicroMalHeur_id)
			  ,[catHash_id] = ISNULL(catHash_id, @removeCatHash_id)
			  ,[smartHash_id] = ISNULL(smartHash_id, @removeSmartHash_id)
		WHERE [id] = @keepFilesystemId

		--Update the filesystem_id in dataset_has_filesystem
		DECLARE myCursor CURSOR FAST_FORWARD FOR 
			SELECT id,dataset_id,pathDS_id,[source],contributor_id,contributorData_id 
			FROM dataset_has_filesystem 
			WHERE filesystem_id = @removeFilesystemId
			
		OPEN myCursor
		FETCH NEXT FROM myCursor INTO @removeDhfId,
									  @removeDataset_id,
									  @removePathDS_id,
									  @removeSourceDhf,
									  @removeContributor_id,
									  @removeContributorData_id
		WHILE @@FETCH_STATUS = 0
		BEGIN
			--UPDATE dhf row with filesystem_id that will be kept
			BEGIN TRY

					UPDATE dataset_has_filesystem
					SET filesystem_id = @keepFilesystemId
					WHERE id = @removeDhfId AND
						  filesystem_id = @removeFilesystemId --Extra safety criteria 
			END TRY
			BEGIN CATCH
					--Handle conflicts in UQ - find duplicate row.
					--DHF UQ is on: filesystem_id, pathDS_id, contributor_id, dataset_id, contributorData_id
					SELECT @keepDhfId = id, 
						   @keepSourceDhf = [source]
					FROM dataset_has_filesystem
					WHERE filesystem_id = @keepFilesystemId AND 
						  pathDS_id = @removePathDS_id AND 
						  contributor_id = @removeContributor_id AND
						  dataset_id = @removeDataset_id AND 						  
						  (contributorData_id = @removeContributorData_id
						  or (@removeContributorData_id IS NULL --NULL permitted in this field
								AND contributorData_id IS NULL)) 

					--Source is not included in dhf UQ.  Want to keep 
					--source data if available.
					IF (@keepSourceDhf IS NULL AND @removeSourceDhf IS NOT NULL)
						UPDATE dataset_has_filesystem
						SET [source] = @removeSourceDhf
						WHERE id = @keepDhfId AND
							  filesystem_id = @keepFilesystemId
							  
					--Before deleting dhf row need to update action rows
					--that link to that dhf row.
					UPDATE action SET dhf_id = @keepDhfId
						WHERE dhf_id = @removeDhfId AND
							  filesystem_id = @removeFilesystemId

					--Remove duplicate dhf row
					DELETE FROM dataset_has_filesystem
					WHERE id = @removeDhfId AND
						  filesystem_id = @removeFilesystemId
			END CATCH
			FETCH NEXT FROM myCursor INTO @removeDhfId,
									  @removeDataset_id,
									  @removePathDS_id,
									  @removeSourceDhf,
									  @removeContributor_id,
									  @removeContributorData_id
		END
		CLOSE myCursor
		DEALLOCATE myCursor

		--Update softwareVersion_has_filesystem
		DECLARE myCursor CURSOR FAST_FORWARD FOR 
			SELECT softwareVersion_id, pathRedo_id, pathDS_id FROM softwareVersion_has_filesystem 
			WHERE filesystem_id = @removeFilesystemId
		OPEN myCursor
		FETCH NEXT FROM myCursor INTO @removeSoftwareVersion_id, @removePathRedo_id, @removePathDS_id
		WHILE @@fetch_status = 0
		BEGIN
			BEGIN TRY
					--UQ on shf is on filesystem_id, softwareversion_id, pathredo_id
					UPDATE softwareVersion_has_filesystem
					SET filesystem_id = @keepFilesystemId
					WHERE softwareVersion_id = @removeSoftwareVersion_id AND
						  pathRedo_id = @removePathRedo_id AND
						  filesystem_id = @removeFilesystemId
			END TRY
			BEGIN CATCH

					SELECT @keepPathDS_id = pathDS_id
					FROM softwareVersion_has_filesystem
					WHERE filesystem_id = @keepFilesystemId AND
						  softwareVersion_id = @removeSoftwareVersion_id AND
						  pathRedo_id = @removePathRedo_id

					IF (@keepPathDS_id IS NULL AND @removePathDS_id IS NOT NULL)
						UPDATE softwareVersion_has_filesystem
						SET pathDS_id = @removePathDS_id
						WHERE filesystem_id = @keepFilesystemId AND
							  softwareVersion_id = @removeSoftwareVersion_id AND
							  pathRedo_id = @removePathRedo_id

					DELETE FROM softwareVersion_has_filesystem
					WHERE softwareVersion_id = @removeSoftwareVersion_id AND
						  pathRedo_id = @removePathRedo_id AND
						  filesystem_id = @removeFilesystemId
			END CATCH
			FETCH NEXT FROM myCursor INTO @removeSoftwareVersion_id,@removePathRedo_id,@removePathDS_id
		END
		CLOSE myCursor
		DEALLOCATE myCursor

		 --update the filesystem_id of action
		UPDATE [dbo].[action]
		SET filesystem_id = @keepFilesystemId
		WHERE filesystem_id = @removeFilesystemId

		--Update the filesystem_id in pe table
		BEGIN TRY --UQ on filesystem_id in pe table
			UPDATE [dbo].[pe]
			SET filesystem_id = @keepFilesystemId
			WHERE filesystem_id = @removeFilesystemId
		END TRY
		BEGIN CATCH
			DECLARE @pe_id BIGINT
			
			SELECT @pe_id = pe_id FROM pe 
			WHERE filesystem_id = @removeFilesystemId

			DELETE FROM pe_directories WHERE pe_id = @pe_id
			DELETE FROM pe_dumps WHERE pe_id = @pe_id
			DELETE FROM pe_export_directories WHERE pe_id = @pe_id
			DELETE FROM pe_exports WHERE pe_id = @pe_id
			DELETE FROM pe_mz WHERE pe_id = @pe_id
			DELETE FROM pe_resource_data_entries WHERE pe_id = @pe_id
			DELETE FROM pe_resource_directories WHERE pe_id = @pe_id
			DELETE FROM pe_sections WHERE pe_id = @pe_id
			DELETE FROM pe_tls_directories WHERE pe_id = @pe_id
			DELETE FROM pe_to_imports WHERE pe_id = @pe_id								
			DELETE FROM pe WHERE pe_id = @pe_id
		
		END CATCH

		--update the installer_id of softwareVersion
		UPDATE [dbo].[softwareVersion]
		SET installer_id = @keepFilesystemId
		WHERE installer_id = @removeFilesystemId

		-- update xfile information
		DECLARE @xfile_id bigint, @xfileLastUpdated datetime, @xfileCount int
		 
		SELECT @xfileLastUpdated = max(lastUpdatedDate), @xfileCount = count(id) 
			FROM filesystem_has_xfile 
			WHERE filesystem_id IN (@keepFilesystemID,@removeFilesystemId)
		
		IF (@xfileCount = 2)
		BEGIN
			SELECT @xfile_id = xfile_id FROM filesystem_has_xfile
			WHERE filesystem_id IN (@keepFilesystemID,@removeFilesystemId)
			AND lastUpdatedDate = @xfileLastUpdated

			DELETE FROM filesystem_has_xfile
			WHERE filesystem_id = @removeFilesystemId

			UPDATE filesystem_has_xfile
			SET xfile_id = @xfile_id
			WHERE filesystem_id = @keepFilesystemId
		END
		ELSE IF (@xfileCount = 1)
		BEGIN
			UPDATE filesystem_has_xfile
			SET filesystem_id = @keepFilesystemID
			WHERE filesystem_id = @removeFilesystemId
		END

		-- Update macro modules data
		If EXISTS(SELECT 1 FROM filesystem_has_macroModule WHERE filesystem_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_macroModule SET filesystem_id = @keepFilesystemId
				WHERE filesystem_id = @removeFilesystemId AND macroModule_id NOT IN (
						SELECT macroModule_id FROM filesystem_has_macroModule 
							WHERE filesystem_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_macroModule data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_macroModule SET filesystem_id = @keepFilesystemId
						WHERE filesystem_id = @removeFilesystemId AND macroModule_id NOT IN (
								SELECT macroModule_id FROM filesystem_has_macroModule 
									WHERE filesystem_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH
						
			DELETE FROM filesystem_has_macroModule WHERE filesystem_id = @removeFilesystemId
		END


		-- Update trid data
		If EXISTS(SELECT 1 FROM filesystem_has_trid WHERE filesystem_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_trid SET filesystem_id = @keepFilesystemId
				WHERE filesystem_id = @removeFilesystemId AND trid_id NOT IN (
						SELECT trid_id FROM filesystem_has_trid 
							WHERE filesystem_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_macroModule data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_trid SET filesystem_id = @keepFilesystemId
						WHERE filesystem_id = @removeFilesystemId AND trid_id NOT IN (
								SELECT trid_id FROM filesystem_has_trid 
									WHERE filesystem_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH
						
			DELETE FROM filesystem_has_trid WHERE filesystem_id = @removeFilesystemId
		END


        -- Update filesystem_has_parent links
		-- Case when it's the file within a parent(archive) file
		If EXISTS(SELECT 1 FROM filesystem_has_parent WHERE filesystem_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_parent SET filesystem_id = @keepFilesystemId
				WHERE filesystem_id = @removeFilesystemId AND filesystem_parent_id NOT IN (
						SELECT filesystem_parent_id FROM filesystem_has_parent 
							WHERE filesystem_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_parent data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_parent SET filesystem_id = @keepFilesystemId
						WHERE filesystem_id = @removeFilesystemId AND filesystem_parent_id NOT IN (
								SELECT filesystem_parent_id FROM filesystem_has_parent 
									WHERE filesystem_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH
			DELETE FROM filesystem_has_parent WHERE filesystem_id = @removeFilesystemId		
		END
		-- Case when it's the parent(archive)
		If EXISTS(SELECT 1 FROM filesystem_has_parent WHERE filesystem_parent_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_parent SET filesystem_parent_id = @keepFilesystemId
				WHERE filesystem_parent_id = @removeFilesystemId AND filesystem_id NOT IN (
						SELECT filesystem_id FROM filesystem_has_parent 
							WHERE filesystem_parent_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_parent data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_parent SET filesystem_parent_id = @keepFilesystemId
						WHERE filesystem_parent_id = @removeFilesystemId AND filesystem_id NOT IN (
								SELECT filesystem_id FROM filesystem_has_parent 
									WHERE filesystem_parent_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH		
			DELETE FROM filesystem_has_parent WHERE filesystem_parent_id = @removeFilesystemId
		END
		

		-- Update filesystem_has_archive links
		-- Case when it's the file within a parent(archive) file
		If EXISTS(SELECT 1 FROM filesystem_has_archive WHERE filesystem_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_archive SET filesystem_id = @keepFilesystemId
				WHERE filesystem_id = @removeFilesystemId AND filesystem_archive_id NOT IN (
						SELECT filesystem_archive_id FROM filesystem_has_archive 
							WHERE filesystem_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_archive data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_archive SET filesystem_id = @keepFilesystemId
						WHERE filesystem_id = @removeFilesystemId AND filesystem_archive_id NOT IN (
								SELECT filesystem_archive_id FROM filesystem_has_archive 
									WHERE filesystem_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH
			DELETE FROM filesystem_has_archive WHERE filesystem_id = @removeFilesystemId		
		END
		-- Case when it's the parent(archive)

		If EXISTS(SELECT 1 FROM filesystem_has_archive WHERE filesystem_archive_id = @removeFilesystemId)
		BEGIN
			BEGIN TRY
				UPDATE filesystem_has_archive SET filesystem_archive_id = @keepFilesystemId
				WHERE filesystem_archive_id = @removeFilesystemId AND filesystem_id NOT IN (
						SELECT filesystem_id FROM filesystem_has_archive 
							WHERE filesystem_archive_id = @keepFilesystemId)
			END TRY
				BEGIN CATCH
					--Only want to catch and handle exception relating to UQ violations.
					--2601 and 2627 are caused by violations in unique constraint/index
					IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
					BEGIN
						-- Try again after short delay, whatever other process modified 
						-- filesystem_has_archive data for this file will hopefully have completed
						WAITFOR DELAY '00:00:02'
						UPDATE filesystem_has_archive SET filesystem_archive_id = @keepFilesystemId
						WHERE filesystem_archive_id = @removeFilesystemId AND filesystem_id NOT IN (
								SELECT filesystem_id FROM filesystem_has_archive 
									WHERE filesystem_archive_id = @keepFilesystemId)
					END
					ELSE
					BEGIN
						SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
							   @ErrorSeverity = ERROR_SEVERITY(),
							   @ErrorState = ERROR_STATE()

						RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
						RETURN -100
					END
				END CATCH		
			DELETE FROM filesystem_has_archive WHERE filesystem_archive_id = @removeFilesystemId
		END
		
    
       
		--Delete the filesystem row
		DELETE FROM filesystem WHERE id = @removeFilesystemId
       
	
		EXECUTE cdm_sp_reason_insert @reason = @reason ,@id = @reason_id OUTPUT
		INSERT INTO action(filesystem_id, actionType_id, users_id, reason_id)
			VALUES(@keepFilesystemId, 
				   @actionType_id,
				   @users_id,
				   @reason_id)
		
		SET @filesystem_id = @keepFilesystemId
		
		/*Verify there is now only 1 filesystem row for that MD5 & SHA256
		If not rerun sproc to merge remaining 2 rows.  Ignore if this is
		already 2nd call of sproc (indicates something went wrong, don't want 
		to get stuck in infinite loop).*/
		IF (@noRepeat IS NULL)
		BEGIN
			SELECT @rowCount = COUNT(id) FROM filesystem WHERE [MD5] = @md5 OR SHA256=@sha256
			IF (@rowCount>'1')
			BEGIN
				EXEC cdm_sp_filesystem_merge
					@md5 = @md5, 
					@sha256 = @sha256,
					@users_id = @users_id,
					@noRepeat =  1,
					@filesystem_id = @filesystem_id OUTPUT
			END
		END		
		--Return relevant filesystem_id, handy if calling sp from a script - no need to create 
		--and assign OUTPUT value to variable etc.
		If @printRes > 0
			SELECT @filesystem_id as 'filesystem_id'
		RETURN @filesystem_id
     END
END

