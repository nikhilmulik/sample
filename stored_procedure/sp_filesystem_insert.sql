SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[cdm_sp_filesystem_insert](
		@users_id TINYINT,
		@reason NVARCHAR(440),
		@contributor_id SMALLINT,
		--optional parameters
		@MD5 NCHAR(32)=NULL,
		@SHA NCHAR(40) = NULL,
        @SHA224 NCHAR(56) = NULL,
		@SHA256 NCHAR(64) = NULL,
		@SHA384 NCHAR(96) = NULL,
		@SHA512 NCHAR(128) = NULL,
		@troj1 NVARCHAR(8) = NULL,
		@troj2 NVARCHAR(8) = NULL,
		@troj4 NVARCHAR(8) = NULL,
		@microMalHeurHash CHAR(32) = NULL,
		@catHash CHAR(40) = NULL,
		@peImageSHA256 NCHAR(64) = NULL,
		@size BIGINT = NULL,
		@attribute SMALLINT = NULL,
		@mime NVARCHAR(127) = NULL,
		@magic NVARCHAR(255) = NULL,
		@xfileOutputData NVARCHAR(4000) = NULL,
		@originalName NVARCHAR(255) = NULL,
		@architecture_id TINYINT = NULL,
		@fileVersion NVARCHAR(255) = NULL,
		@companyName NVARCHAR(255) = NULL,
		@productName NVARCHAR(255) = NULL,
		@productVersion NVARCHAR(255) = NULL,
		@description NVARCHAR(255) = NULL,
		@languageCode CHAR(4) = NULL,
		@parentMD5 NCHAR(32) = NULL,
		@pathWithinParent NVARCHAR(1163) = NULL,
		@macroModulesData NVARCHAR(MAX) = NULL,
		@tridOutputData NVARCHAR(MAX) = NULL,
		@source NVARCHAR(255) = NULL,
		@trust_id TINYINT = 3,
		@full_info TINYINT = 0,
		@signature_id BIGINT = NULL,
		@gcrcData_id BIGINT = NULL,
		@gvmCRCData_id BIGINT = NULL,
		@dhf_id BIGINT = NULL,
		@softwareVersion_id INT = NULL,
        @filesystem_id BIGINT = NULL OUTPUT,
        @active TINYINT = NULL,
        @printRes TINYINT = 0,
        @err INT = NULL OUTPUT
)
AS
BEGIN


    --Converting input parameter @macroModulesData NVARCHAR to XML 
    SET @macroModulesData = NULLIF(@macroModulesData,'')
	DECLARE @macroModulesData_XML XML
	SET @macroModulesData_XML = Convert(XML,@macroModulesData)
	
	--Converting input parameter @tridOutputData NVARCHAR to XML
	SET @tridOutputData = NULLIF(@tridOutputData,'')
	DECLARE @tridOutputData_XML XML
	SET @tridOutputData_XML = Convert(XML,@tridOutputData)

    -- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	--check required fields
	IF @MD5 IS NULL AND @SHA256 IS NULL
		BEGIN
			RAISERROR ('MD5 or SHA256 is required',16,1)
			RETURN -100
		END

	IF @users_id IS NULL
		BEGIN
			RAISERROR ('users_id is a required parameter, please check the USERS table.',16,1)
			RETURN -100
		END

	IF @reason IS NULL
		BEGIN
			RAISERROR ('reason is a required parameter.',16,1)
			RETURN -100
		END

	IF @contributor_id IS NULL
		BEGIN
			RAISERROR ('contributor_id is a required parameter, please check the CONTRIBUTOR table.',16,1)
			RETURN -100
		END
    -- Insert data to filesystem
	BEGIN TRANSACTION
		select TOP 1 @filesystem_id=[id] from filesystem where MD5=@MD5 or SHA256=@SHA256
		IF @@RowCount > 0
			BEGIN
				DECLARE @fuptbl TABLE (
					filesystem_id BIGINT,	--Need this in case a merge took place
					rowNum int,
					error int
				)
				INSERT INTO @fuptbl
				EXEC cdm_sp_filesystem_updateMetadata @filesystem_id=@filesystem_id,@MD5=@MD5,@SHA256=@SHA256
				,@SHA=@SHA,@SHA224=@SHA224,@SHA384=@SHA384,@SHA512=@SHA512,@troj1=@troj1,@troj2=@troj2,@troj4=@troj4
				,@microMalHeurHash=@microMalHeurHash,@catHash=@catHash,@languageCode=@languageCode,@size=@size
				,@attribute=@attribute,@mime=@mime,@magic=@magic,@xfileOutputData=@xfileOutputData,@originalName=@originalName
				,@architecture_id=@architecture_id,@fileVersion=@fileVersion,@companyName=@companyName
				,@productName=@productName,@productVersion=@productVersion,@description=@description
				,@macroModulesData=@macroModulesData,@tridOutputData=@tridOutputData,@source=@source,@parentMD5=@parentMD5
				,@pathWithinParent=@pathWithinParent,@trust_id=@trust_id,@full_info=@full_info
				,@gcrcData_id=@gcrcData_id,@gvmCRCData_id=@gvmCRCData_id,@softwareVersion_id=@softwareVersion_id
				,@signature_id=@signature_id,@users_id=@users_id,@reason=@reason,@contributor_id=@contributor_id
				,@dhf_id=@dhf_id,@peImageSHA256 = @peImageSHA256, @active=@active
				
				--filesystem id may have changed if merge of filesystem rows took place
				SELECT @filesystem_id = filesystem_id FROM @fuptbl
			END
		ELSE
			BEGIN
                DECLARE @mime_id INT
				DECLARE @magic_id INT
				DECLARE @peVersionInfo_id INT
				DECLARE @microMalHeur_id INT
				DECLARE @catHash_id INT
				DECLARE @smartHash_id INT
				EXECUTE cdm_sp_mime_insert @mime = @mime ,@id = @mime_id OUTPUT,@printRes = @printRes
				EXECUTE cdm_sp_magic_insert @magic = @magic ,@id = @magic_id OUTPUT,@printRes = @printRes
				EXECUTE cdm_sp_peVersionInfo_insert @originalName = @originalName,@fileVersion = @fileVersion,@companyName = @companyName,@productName = @productName,
                @productVersion = @productVersion, @description = @description,@languageCode=@languageCode,@id = @peVersionInfo_id OUTPUT ,@printRes = @printRes
				EXECUTE cdm_sp_micromalheur_insert @hash = @microMalHeurHash, @id = @microMalHeur_id OUTPUT,@printRes = @printRes
				EXECUTE cdm_sp_cathash_insert @hash = @catHash, @id = @catHash_id OUTPUT,@printRes = @printRes
				EXECUTE cdm_sp_smarthash_insert @peImageSHA256 = @peImageSHA256, @smartHash_id = @smartHash_id OUTPUT, @printRes = @printRes
				INSERT INTO [dbo].[filesystem]
					   ([size]
					   ,[MD5]
					   ,[SHA]
					   ,[SHA224]
					   ,[SHA256]
					   ,[SHA384]
					   ,[SHA512]
					   ,[troj1]
					   ,[troj2]
					   ,[troj4]
					   ,[attribute]
					   ,[mime_id]
					   ,[magic_id]
					   ,[architecture_id]
					   ,[peVersionInfo_id]
					   ,[source]
					   ,[trust_id]
					   ,[full_info]
					   ,[signature_id]
					   ,[gcrcData_id]
					   ,[gvmCRCData_id]
					   ,[microMalHeur_id]
					   ,[catHash_id]
					   ,[smartHash_id])
				 VALUES
					   (@size
					   ,@MD5
					   ,@SHA
					   ,@SHA224
					   ,@SHA256
					   ,@SHA384
					   ,@SHA512
					   ,@troj1
					   ,@troj2
					   ,@troj4
					   ,@attribute
					   ,@mime_id
					   ,@magic_id
					   ,@architecture_id
					   ,@peVersionInfo_id
					   ,@source
					   ,@trust_id
					   ,@full_info
					   ,@signature_id
					   ,@gcrcData_id
					   ,@gvmCRCData_id
					   ,@microMalHeur_id
					   ,@catHash_id
					   ,@smartHash_id)
				SET @err = @@Error
				IF @err <>0
					BEGIN
						ROLLBACK TRANSACTION
						SET @filesystem_id = -1
						GOTO ErrorHandler
					END
				SET @filesystem_id = SCOPE_IDENTITY();
				IF @err <>0
					BEGIN
						ROLLBACK TRANSACTION
						SET @filesystem_id = -1
						GOTO ErrorHandler
					END
					
				DECLARE @reason_id INT
					
				IF @SHA256 IS NOT NULL
					BEGIN
                        EXECUTE cdm_sp_reason_insert @reason = @reason ,@id = @reason_id OUTPUT,@printRes = @printRes
						INSERT INTO [dbo].[action]
							   ([filesystem_id]
							   ,[actionType_id]
							   ,[users_id]
							   ,[reason_id]
							   ,[dhf_id]
							   ,[contributor_id]
							   ,[softwareVersion_id])
						 VALUES
							   (@filesystem_id
							   ,7 --ActionType for adding SHA256
							   ,@users_id
							   ,@reason_id
							   ,@dhf_id
							   ,@contributor_id
							   ,@softwareVersion_id)
						IF @err <>0
							BEGIN
								ROLLBACK TRANSACTION
								GOTO ErrorHandler
							END
					END
					
				IF @smartHash_id IS NOT NULL
					BEGIN
                        EXECUTE cdm_sp_reason_insert @reason = @reason ,@id = @reason_id OUTPUT,@printRes = @printRes
						INSERT INTO [dbo].[action]
							   ([filesystem_id]
							   ,[actionType_id]
							   ,[users_id]
							   ,[reason_id]
							   ,[dhf_id]
							   ,[contributor_id]
							   ,[softwareVersion_id])
						 VALUES
							   (@filesystem_id
							   ,10	--ActionType for adding PEImage Smarthash
							   ,@users_id
							   ,@reason_id
							   ,@dhf_id
							   ,@contributor_id
							   ,@softwareVersion_id)
						IF @err <>0
							BEGIN
								ROLLBACK TRANSACTION
								GOTO ErrorHandler
							END
					END

				IF @xfileOutputData IS NOT NULL AND @filesystem_id > 0
					BEGIN
						EXECUTE cdm_sp_xfile_insert @filesystem_id = @filesystem_id, @xfileOutputData = @xfileOutputData
					END
					
				IF @macroModulesData IS NOT NULL AND @filesystem_id > 0
					BEGIN
						EXECUTE cdm_sp_macro_modules_insert @filesystem_id = @filesystem_id, @macroModulesData = @macroModulesData_XML	
					END	
					
				IF @tridOutputData IS NOT NULL AND @filesystem_id > 0
					BEGIN
						EXECUTE cdm_sp_trid_insert @filesystem_id = @filesystem_id, @tridOutputData = @tridOutputData_XML	
					END				

				IF @parentMD5 IS NOT NULL AND @filesystem_id > 0
					BEGIN
						-- If the parent file does not already exist in CDM need to add it before calling linker SP
						IF NOT EXISTS (SELECT 1 FROM filesystem WHERE md5 = @parentMD5)
						BEGIN							
							BEGIN TRY
								DECLARE @filesystemIdParent TABLE(id BIGINT)
								INSERT INTO filesystem(MD5) OUTPUT inserted.id into @filesystemIdParent VALUES(@parentMD5)	
								-- Must insert related add action
								SET @reason = 'Inserting Parent MD5. Upload reason for file(' +ISNULL(@MD5,@SHA256) +') within: '+@reason
								EXECUTE cdm_sp_reason_insert @reason=@reason, @id=@reason_id OUTPUT, @printRes=@printRes
								
								INSERT INTO [action](filesystem_id, contributor_id, reason_id, users_id, actionType_id) 
									SELECT id, @contributor_id, @reason_id, @users_id, 1 FROM @filesystemIdParent
							END TRY
							BEGIN CATCH
								--Only want to catch and handle exception relating to UQ violations.
								--2601 and 2627 are caused by violations in unique constraint/index
								IF (ERROR_NUMBER() = 2601 OR ERROR_NUMBER() = 2627)
								BEGIN
									IF NOT EXISTS (SELECT 1 FROM filesystem WHERE md5 = @parentMD5)
										BEGIN
											ROLLBACK TRANSACTION
											RAISERROR('Failed to insert parent MD5 %s for file with MD5 %s.  
											UQ violation occured yet parent does not exist in the filesystem table.', 
											16, 8, @parentMD5, @MD5)  
											RETURN -100  
										END
								END
								ELSE
								BEGIN
									DECLARE @ErrorMessage NVARCHAR(max), @ErrorSeverity INT, @ErrorState INT
									SELECT @ErrorMessage = ERROR_MESSAGE() + ' Line ' + cast(ERROR_LINE() as nvarchar(5)),
										   @ErrorSeverity = ERROR_SEVERITY(),
										   @ErrorState = ERROR_STATE()
									ROLLBACK TRANSACTION
									RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState)
									RETURN -100
								END
							END CATCH
						END
						EXECUTE cdm_sp_link_to_parent @filesystem_id = @filesystem_id, @parentMD5 = @parentMD5, @pathWithinParent = @pathWithinParent
					END		
				END

	COMMIT TRANSACTION
	SET @err = NULL
	SELECT @filesystem_id as 'filesystem_id', @err as 'error'
	RETURN 0
ErrorHandler:
	SET @err = -100
END


