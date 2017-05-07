#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
crawlDS

this script crawls a directory on a disk, visits all directories and,
for each file, the script extracts lowlevel info and some higher level info
in the case of executable files
'''

import logging
import os
import time
import re
import sys
import csv
import collections
import pprint

try:
    import json
except ImportError:
    import simplejson as json

import symscan
import UniExtract

from crawler.cli import parseOpts, getJSONOfOpt
from crawler.timing import timefunc
from crawler.meta_headers import META_LIST_HEADERS
from crawler.file_utils import split_file_path, rmtree
from crawler.errors import CrawlDSError
from crawler import file_utils
from crawler import progress
from crawler.filepath import FilePath


MAX_COPY_ATTEMPTS = 5


class InfectedFileFoundException(CrawlDSError):
    """
    An exception when a detected file is found
    """
    pass


def delete_decompress_folder():
    return True


def num_to_letter(num):
    num = num-1
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    letters = len(alphabet)
    if num >= letters:
        return num_to_letter(num//letters)+num_to_letter((num%letters)+1)
    return alphabet[num]

####################################################################################
####################################################################################
####################################################################################

class Crawler(object):
    """
    The crawler process list of FilePaths
     it does not deal with decompressing or skipping files or scanning for infected files
    """
    def __init__(self, file_paths, opts, timers=None, one_csv_file=None):
        self._options = opts
        #
        self.all_file_paths = file_paths
        if timers is None:
            self.timers = {}
        else:
            self.timers = timers
        self.one_csv_file = one_csv_file

    def nondir_filepaths(self):
        """
        A generator for file paths that are not directories
        """
        for file_path in self.all_file_paths:
            if not file_path.isdir():
                yield file_path

    def pefiles_filepaths(self):
        """
        A generator for PE files in that all file paths list
        """
        for file_path in self.nondir_filepaths():
            if file_path.isPEfile():
                yield file_path

    def crawl(self):
        """
        Creates the output folder and processes all files
        """
        if not os.path.isdir(self._options.output) and not self._options.one_csv:
            if len(self._options.output) > 239:
                msg = ("The file path for the output is too long, you must shorten it. "
                       "The outputted files will be unreadable by nearly every system (%d) %s\nCrawler will now exit " %
                       (len(self._options.output), self._options.output))
                logging.error(msg)
                print msg
                sys.exit(1)
            try:
                os.makedirs(self._options.output)
            except OSError:
                logging.fatal("Cannot create output folder; exiting ...")
                print "Cannot create output folder; exiting ..."
                sys.exit(1)
        elif self._options.one_csv:
            if not os.path.exists(self._options.one_csv):
                dir_path = os.path.dirname(self._options.one_csv)
                if not os.path.exists(dir_path):
                    try:
                        os.makedirs(dir_path)
                    except OSError:
                        logging.fatal("Cannot create output folder; exiting ...")
                        print "Cannot create output folder; exiting ..."
                        sys.exit(1)
            if file_utils.is_filepath_too_long(self._options.one_csv):
                msg = "The file path for the one csv is too long and will not be readable in windows, please shorten it"
                msg += " (%d) %s" % (len(self._options.one_csv), self._options.one_csv)
                logging.error(msg)
                print msg
                sys.exit(1)
        self.process_all_files()

    @timefunc("Getting PE file versions")
    def get_file_versions(self):
        """
        Get PE file version information 
        """
        if not self._options.pe:
            return
        for path in self.all_file_paths:
            if not path.isdir():
                path.get_file_version()

    @timefunc("Getting magic file type info")
    def get_magics(self):
        """
        Get architecture ie 64 or 32 bit and magic for all file paths
        """
        if self._options.magic or self._options.architecture:
            logging.debug("Getting magic info")
            for file_path in self.all_file_paths:
                if not file_path.isdir():
                    file_path.get_magic()
                    if file_path.isPEfile():
                        file_path.get_arch()

    @timefunc("Getting mime info")
    def get_mimes(self):
        """
        Get mime info for all file paths
        """
        if self._options.mime:
            logging.debug("Getting mime")
            for file_path in self.nondir_filepaths():
                file_path.get_mime()

    @timefunc("Getting gvm CRC")
    def get_crcs(self):
        """
        Get gvm CRC for all file paths 
        """
        if self._options.gvmCRC:
            for file_path in self.nondir_filepaths():
                file_path.get_crc()

    @timefunc("Getting file sizes")
    def get_sizes(self):
        """
        Get file sizes for all file paths
        """
        if self._options.size:
            for file_path in self.nondir_filepaths():
                file_path.get_size()

    @timefunc("Getting smart hashes")
    def get_smart_hashes(self):
        if self._options.smarthash:
            for file_path in self.nondir_filepaths():
                file_path.get_smarthash()

    @timefunc("Getting file attributes")
    def get_attributes(self):
        """
        Get attributes for all file paths
        """
        if self._options.attribute:
            for file_path in self.all_file_paths:
                file_path.get_attributes()

    @timefunc("Getting cat hashes")
    def get_all_catHash_hashs(self):
        """
        Get catHash for all file paths
        """
        if self._options.catHash:
            for file_path in self.nondir_filepaths():
                file_path.get_catHash_hash()

    @timefunc("Getting md5s")
    def get_md5s(self):
        """
        Get md5s for all file paths
        """
        if self._options.md5:
            for file_path in self.nondir_filepaths():
                file_path.get_md5()

    @timefunc("Getting sha hashes")
    def get_all_all_hashes(self):
        """
        Get sha hashes for all file paths 
        """
        if self._options.sha or self._options.sha2:
            for file_path in self.nondir_filepaths():
                file_path.get_all_hashes(sha1=self._options.sha,
                                         sha2=self._options.sha2)

    @timefunc("Creating json files for PE info")
    def create_json_files(self):
        """
        Create json files for PE information 
        """
        if self._options.header:
            folder = self._options.header
            try:
                os.makedirs(folder, 777)
            except OSError:
                logging.debug("Unable to create directories (it probably already exists)'%s' ", folder)

            for file_path in self.nondir_filepaths():
                file_path.create_json_file(self._options.header)

    @timefunc("Getting troj defs")
    def get_troj_defs(self):
        """
        Get trojan defs for all files
        """
        if self._options.troj:
            for file_path in self.nondir_filepaths():
                file_path.get_troj_def()

    @timefunc("Getting xfile outputdata")
    def get_xfile(self):
        if self._options.xfile:
            for file_path in self.nondir_filepaths():
                file_path.get_xfile()

    @timefunc("Getting macro information")
    def get_macros(self):
        if self._options.macros:
            for file_path in self.nondir_filepaths():
                file_path.get_macros(self._options.uniqueFilesBase)

    @timefunc("Getting gCRCs")
    def get_gcrcs(self):
        """
        Get gGRC for PE files 
        """
        if self._options.gcrc:
            for file_path in self.pefiles_filepaths():
                file_path.get_gcrc()

    @timefunc("Copying files to unique location")
    def copy_to_unique(self):
        """
        Copy the files to a unique location based on their md5
        """
        if self._options.uniqueFilesBase:
            if file_utils.is_filepath_too_long(self._options.uniqueFilesBase):
                logging.warning("The file path for the unique file location is too long for windows %s",
                                self._options.uniqueFilesBase)
                path = file_utils.get_uni_path(self._options.uniqueFilesBase)
            else:
                path = self._options.uniqueFilesBase
            try:
                os.makedirs(path)
            except OSError:
                pass
            if not os.path.exists(path):
                raise CrawlDSError("Cannot create directory for unique file base '%s'" % self._options.uniqueFilesBase)
            if os.path.isfile(path):
                raise CrawlDSError("The directory for unique file base is a file '%s'" % self._options.uniqueFilesBase)
            for file_path in self.nondir_filepaths():
                if not file_path.from_archive:
                    file_path.copy_to_unique(path, self._options.oldUniqueFilesBase)

    def get_dirpath_map(self):
        """
        Returns a dictionary with the key being the directory the files are 
         and the values bing a list of file paths
        """
        result = collections.defaultdict(list)
        for file_path in self.nondir_filepaths(): 
            result[file_path.dirname()].append(file_path)
        return dict(result)

    def write_one_csv(self):
        logging.debug("Writing one csv")
        write_header = not os.path.exists(self.one_csv_file)
        self.create_csv_file(self.one_csv_file, self.nondir_filepaths(), write_header, 'ab')

    def create_csv_file(self, csvname, filepaths, write_header=True, mode='wb'):
        #with codecs.open(csvname, mode="wb", encoding="utf8") as csvfile:
        with open(csvname, mode=mode) as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL, escapechar='\\', doublequote=False)
            if write_header:
                csvwriter.writerow(META_LIST_HEADERS)
            for path in filepaths:
                path.csvwriteurows(csvwriter)

    def write_multi_csvs(self):
        if not self._options.output:
            raise CrawlDSError("No output set")
        output = self._options.output
        folder_count = 0
        folder_num = 0
        if not os.path.exists(output):
            os.makedirs(output)
        output = os.path.abspath(output)
        logging.debug("Writing csv")
        dirmaps = self.get_dirpath_map()
        if dirmaps and self._options.max_csv_files != 0:
            folder_count = len(os.listdir(output))
        for i, dirpath in enumerate(dirmaps):
            # ----------get output folder----------
            if self._options.max_csv_files <= folder_count and self._options.max_csv_files != 0:
                folder_num += 1
                folder_count = 0
                output = os.path.join(self._options.output, "%02d" % folder_num)
                for _ in xrange(10000):
                    output = os.path.join(self._options.output, "%02d" % folder_num)
                    if not os.path.exists(output):
                        break
                    if len(file_utils.get_exts_in_folder(output, '.csv')) < self._options.max_csv_files:
                        break
                    folder_num += 1
                if not os.path.exists(output):
                    os.mkdir(output)
            # -------------------------------------
            folder_count += 1
            i += 1
            csvname = os.path.join(output, "%010d.csv" % i)
            if os.path.exists(csvname):
                #This reached when the file chunk is set
                for j in xrange(1, 1000):
                    letter = num_to_letter(j)
                    csvname = os.path.join(output, "%010d_%s.csv" % (i, letter))
                    if not os.path.exists(csvname):
                        break
                if os.path.exists(csvname):
                    raise CrawlDSError("Too many files for csv writing")

            self.create_csv_file(csvname, dirmaps[dirpath])

    @timefunc("Writing CSVs")
    def write_csvs(self):
        """
        Write the csv files for all the files
        """
        if self._options.one_csv:
            return self.write_one_csv()
        else:
            self.write_multi_csvs()

    def process_all_files(self):
        """
        Process all the files
        """
        self.get_sign_info()
        self.get_file_versions()
        self.get_magics()
        self.get_mimes()
        self.get_crcs()
        self.get_sizes()
        self.get_attributes()
        self.get_smart_hashes()
        self.get_all_catHash_hashs()
        self.get_md5s()
        self.get_all_all_hashes()
        self.create_json_files()
        self.get_troj_defs()
        self.get_gcrcs()
        self.get_xfile()
        self.get_macros()
        self.copy_to_unique()
        self.write_csvs()


    @timefunc("Getting sign info")
    def get_sign_info(self):
        """
        Get the signature information for the file paths
        The signatures of the files are analysed together in one subprocess for speed reasons.
        """
        if self._options.sig:
            logging.debug("Getting sign info")
            for path in self.all_file_paths:
                if not path.isdir(): #and path.isPEfile():
                    path.get_sign_info()


def set_logging(options):
    """
    Setup the logging for log to file or to output
    returns a list of new handlers
    """
    handlers = []
    logLevels = {'debug': logging.DEBUG,
                 'info': logging.INFO,
                 'warning': logging.WARNING,
                 'error': logging.ERROR,
                 'critical': logging.CRITICAL}
    
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    if options.logfile:
        logLevel = options.logLevel.lower()
        logfile_path = options.logfile
        dirpath = os.path.dirname(logfile_path)
        if dirpath:
            if not os.path.exists(dirpath):
                try:
                    os.makedirs(dirpath)
                except OSError:
                    raise CrawlDSError("Could not create directory for log file %s" % dirpath)
        if len(options.logfile) > 254:
            print "The log file name is very long which could cause issues with other programs, please shorten it"
            options.logfile = u"\\\\?\\" + unicode(options.logfile)
        file_handler = logging.FileHandler(options.logfile)
        file_handler.setLevel(logLevels[logLevel])
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s',
                                      '%Y/%m/%d %H.%M.%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        handlers.append(file_handler)
    if options.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        logger.addHandler(stream_handler)
        handlers.append(stream_handler)
    if not options.logfile and not options.verbose:
        logger.setLevel(logging.WARNING)
    return handlers


class CrawlMaster(object):
    """
    The crawl master is for controlling the Crawler object.
    It decompresses files, finds infected files and gets chunks of files to be
        analysed by the Crawler so the Crawler just deals with analysing lists of FilePaths
    """
    def __init__(self, rootdirs, options, filelist_crawl_enabled=False):
        self.start = time.time()
        self.timers = {}
        # rootdirs will contain list of directory or list of files also when filelist_crawl_enabled is set to True
        self.rootdirs = [unicode(rd) for rd in rootdirs]
        self.options = options
        # TODO: change to a set
        self.analysed_files = []
        #self.compressed_files = []
        #self.all_file_paths = []
        self.arc_file_md5s = set([])
        self.arc_file_paths = []
        self.arc_file_map = collections.defaultdict(list)
        self._decomp_temp_dir = None
        self.infected_files = []
        self._symscanner = None
        self.one_csv_filename = None
        #Files to exclude from crawling
        self.reDecompExclude = re.compile(r"(!)|(\.data)|(\.debug)|(\.idata)|(\.bss)|(\.orpc)|(\.pdata)|(\.rdata)|"
                                          r"(\.reloc)|(\.rsrc)|(\.rodata)|(\.text)|(^CERTIFICATE$)|(^INIT$)|"
                                          r"(^PAGE$)|(^AUTHORS$)|(^NEWS$)")
        self.filter_out_folder = options.filter_out_folder
        if self.filter_out_folder:
            self.filter_out_folder = self.filter_out_folder.replace(",,", "|")
            self.filter_out_folder = self.filter_out_folder.split(',')
            self.filter_out_folder = [i.replace('|', ',') for i in self.filter_out_folder]
        self.progress = None
        self._recovery_path = None
        if self.options.progress:
            self.progress = progress.Progress()
        self.filelist_crawl_enabled = filelist_crawl_enabled

    @property
    def decomp_temp_dir(self):
        """
        A property that is the directory path to the temporary decompression folder
        """
        if self.options.decomp:
            self._decomp_temp_dir = FilePath(self.options.decomp)
        return self._decomp_temp_dir

    @property
    def recovery_file_path(self):
        """
        A property that is the recovery file path
        """
        json_basename = u'recovery_point.json'
        if self._recovery_path is None:
            self._recovery_path = os.path.abspath(self.options.output)
            tpath = os.path.join(self.options.output, json_basename)
            if file_utils.is_filepath_too_long(tpath):
                self._recovery_path = file_utils.get_uni_path(self._recovery_path)
            if not os.path.exists(self._recovery_path):
                os.makedirs(self._recovery_path)
            self._recovery_path = os.path.join(self._recovery_path, json_basename)
        return self._recovery_path

    @property
    def symscanner(self):
        """
        A property that is the symscanner object
        """
        if self._symscanner is None:
            self._symscanner = symscan.scanner(symscan=self.options.symscan,
                                               defs=self.options.symscan_defs,
                                               move_detected=self.options.detected_files,
                                               logger=logging,
                                               verbose=self.options.verbose)
        return self._symscanner

    def cleanup(self):
        """
        Delete the temporary decompression folder
        """
        if self.options.decomp and delete_decompress_folder():
            rmtree(self.decomp_temp_dir.sys_file_path, keepdir=True)
        self.arc_file_map = collections.defaultdict(list)

    def update_recovery(self, file_paths=None):
        """
        Update the recovery file
        """
        if file_paths:
            for fp in file_paths:
                self.analysed_files.append(fp.file_path)
        try:
            with open(self.recovery_file_path, 'w') as fp:
                json.dump({'analysed_files':self.analysed_files}, fp)
        except IOError:
            logging.warning("Unable to update recovery json file")

    def update_from_recovery(self):
        """
        Find files that have already been analysed
            based on the recovery file which is a json file passed as an command line argument
        """
        if not self.options.recovery_point:
            return
        try:
            with open(self.options.recovery_point, 'r') as fp:
                recovery_info = json.load(fp)
        except IOError:
            logging.warning("Cannot open file '%s'", self.options.recovery_point)
            return
        except ValueError:
            logging.warning("Corrupted json file '%s'", self.options.recovery_point)
            return
        try:
            self.analysed_files = recovery_info['analysed_files']
        except TypeError:
            logging.warning("analysed_files not in json file'%s'", self.options.recovery_point)
            return
        self.update_recovery()

    def get_infected_files(self, dirpath):
        """
        Use symscanner to scan the directory dirpath
            and return a list of file paths
            the return file paths are sting values not FilePath objects
        """
        if self.options.symscan:
            logging.debug("Scanning %s", dirpath)
            root_path = FilePath(dirpath)
            to_scan = root_path.file_path
            if to_scan[-1] == "\\":
                to_scan = to_scan + "\\"
            scan_result = self.symscanner.scan(to_scan)
            if scan_result == 0:
                if not (os.path.isdir(to_scan) and len(os.listdir(to_scan))==0):
                    logging.error("Error running sym scan! Possible malicious ")
            result = self.symscanner.parse(scan_result)
            if result:
                files = result.get('Files', [])[:]
                if files:
                    logging.warning("!MALICIOUS FILES FOUND!")
                    logging.warning("Full scan output:\n%s", scan_result)
                    logging.warning(pprint.pformat(result))
                else:
                    logging.info("Sym scan:")
                    for name in ['Defs_Date', 'Defs_Version', 'Scan_Mode']:
                        logging.info("%s:%s", name, result.get(name, 'unknown'))
                # files is list of dictionary with all details of detected files as type of detection, md5, sha256
                # Extracting just file path from dictionary and appending it to infected_files list so those infected
                # file get EXCLUDED while crawling.
                file_list = [file_['File'] for file_ in files]
                self.symscanner.moveDetected(files)
                self.infected_files.extend(file_list)
                return files
        return []

    def is_path_filtered(self, path):
        if not self.filter_out_folder:
            return False
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        path = os.path.abspath(path)
        filenames = path.split(os.sep)
        for fil in self.filter_out_folder:
            if fil in filenames:
                return True
        return False

    def get_file_count_estimate(self):
        count = 0
        if not self.filelist_crawl_enabled:
            for rootdir in self.rootdirs:
                for base, _, files in os.walk(rootdir):
                    if not self.is_path_filtered(base):
                        count += len(files)
        else:
            count = len(self.rootdirs)
        return count

    def update_all_file_paths(self):
        """
        Get all file paths in root directories
        Also checks for recovery file and infected files (infected files are ignored)
        """
        self.update_from_recovery()
        rootdirs = self.rootdirs
        #dir_paths = []
        if self.options.symscan and not self.options.scanArchivesOnly:
            for path in self.rootdirs:
                self.get_infected_files(path)
        if not self.filelist_crawl_enabled:
            for rootdir in rootdirs:
                for base, _, files in os.walk(rootdir):
                    if not self.is_path_filtered(base):
                        for file_ in files:
                            new_path = os.path.join(base, file_)
                            if not new_path in self.analysed_files and not new_path in self.infected_files:
                                fp = FilePath(new_path, rootdir, wsus_path=self.options.wsus_path,
                                              no_xfile=self.options.no_xfile)
                                if not fp.is_zero_file():
                                    yield fp
                    else:
                        logging.info("Filtered out the folder '%s'", base)
        else:
            for new_path in self.rootdirs:
                if not self.is_path_filtered(os.path.dirname(new_path)):
                    if not new_path in self.analysed_files and not new_path in self.infected_files:
                        fp = FilePath(new_path,os.path.dirname(new_path), wsus_path=self.options.wsus_path,
                                      no_xfile=self.options.no_xfile)
                        if not fp.is_zero_file():
                            yield fp
                else:
                    logging.info("Filtered out the folder '%s'", os.path.dirname(new_path))

    @timefunc("Decompress files")
    def decompress_file(self, filePath, depth=None, new_paths=None):
        """
        Decompress the filePath
        this function is recursive and the depth and new_paths is used during recursion
        Returns a list of filePaths that have been decompressed
        """
        skip_folders = [".rsrc", ".RSRC", "CERTIFICATE"]

        def is_skip_path(path):
            paths = split_file_path(path)
            for skip_folder in skip_folders:
                if skip_folder in paths:
                    return True
            return False
        if new_paths is None:
            new_paths = []
        if depth is None:
            depth = [0]
        if depth[0] >= int(self.options.depth):
            depth[0] = 0
            logging.warning("The maximum depth for decompression (%d) has been reached: %s" % (int(self.options.depth),
                                                                                               repr(filePath)))
            return []

        depth[0] += 1
        if filePath.md5 in self.arc_file_md5s:
            logging.warning("Archive file has already been decompressed: %s", filePath)
            return []
        self.arc_file_md5s.add(filePath.md5)
        self.arc_file_paths.append(filePath)

        # decompress a file into "targetdir". Creates dirs, files and subdirs. Returns bool.
        # logging.debug("The temp decompress path=%s", self.decomp_temp_dir.file_path)
        targetdir = filePath.get_target_dir(self.decomp_temp_dir.file_path)
        decomp_path = filePath.file_path
        logging.debug("Attempting to extract '%s' to '%s'", decomp_path, targetdir)
        uniextract = UniExtract.decompose(decomp_path, targetdir,
                                          self.decomp_temp_dir.sys_file_path, verbose=self.options.verbose)
        logging.debug("Uniextract result=%s", uniextract)
        is_exe = os.path.basename(filePath.sys_file_path).split(".")[-1].lower() == "exe"
        for base, _, files in os.walk(targetdir):
            if not is_skip_path(base):
                for file_ in files:
                    new_path = os.path.join(base, file_)
                    if not(is_exe and self.reDecompExclude.match(file_)):
                        new_file_path = FilePath(new_path, targetdir, from_archive=filePath,
                                                 wsus_path=self.options.wsus_path,
                                                 no_xfile=self.options.no_xfile)
                        if new_file_path.check_file() and not new_file_path.is_zero_file():
                            self.arc_file_map[filePath].append(new_file_path)
                            new_paths.append(new_file_path)
                            if new_file_path.is_compressed():
                                logging.debug("Found compressed file '%s'", new_file_path.file_path)
                                self.decompress_file(new_file_path, depth, new_paths)
                            # Add link to the parentMD5 file
                            new_file_path._parentMD5 = filePath.md5
        if self.get_infected_files(targetdir):
            self.infected_files.append(filePath.file_path)
            new_paths = []
            logging.warning("Infected file found %s", filePath.file_path)
            #TODO: Probably should be a better way to do this
            raise InfectedFileFoundException(filePath.file_path)
        return new_paths

    def is_decomp_folder_too_big(self):
        """
        Check if the current decompress temp folder is bigger then
            max_decomp_size_gb argument allows
        """
        if self.decomp_temp_dir:
            return float(self.options.max_decomp_size_gb) <= self.decomp_temp_dir.get_gb_size()
        return False

    def get_file_chunk(self):
        """
        A generator for list of file paths
        It yields lists of FilePaths of len options.file_chunks
        except if the file is compressed then it will return all the files in decompressed
        """
        file_paths = []
        decomp_paths = []
        for file_path in self.update_all_file_paths():
            if file_path.check_file():
                file_paths.append(file_path)
            if file_path.is_compressed() and self.options.decomp:
                try:
                    res = self.decompress_file(file_path)
                    decomp_paths.extend(res)
                except InfectedFileFoundException:
                    logging.warning("Infected file found")
                    file_paths.remove(file_path)
                else:
                    if self.is_decomp_folder_too_big():
                        logging.warning("Decomp temp folder is over %sGB", self.options.max_decomp_size_gb)
                        yield decomp_paths + file_paths
                        decomp_paths = []
                        file_paths = []
                        continue
            if len(file_paths) == int(self.options.file_chunks):
                yield decomp_paths + file_paths
                decomp_paths = []
                file_paths = []
        if file_paths or decomp_paths:
            yield decomp_paths + file_paths

    def get_one_csvfile_path(self):
        if self.options.one_csv:
            return self.options.one_csv

    def crawl(self):
        """
        Crawl through all files
        """
        self.check_all()
        if self.progress:
            self.progress.estimate_num_files = self.get_file_count_estimate()
        for file_paths in self.get_file_chunk():
            for fp in file_paths:
                logging.debug("File path to crawl:'%s'", fp.file_path)
            if self.progress:
                self.progress.new_crawl(len(file_paths))
            crawler = Crawler(file_paths, self.options, self.timers, self.get_one_csvfile_path())
            crawler.crawl()
            self.update_recovery(file_paths)
            self.cleanup()
            if self.progress:
                self.progress.end_crawl()
        try:
            os.remove(self.recovery_file_path)
        except OSError:
            logging.warning("Cannot delete the recovery file path '%s'", self.recovery_file_path)
        try:
            if not os.listdir(os.path.dirname(self.recovery_file_path)):
                os.rmdir(os.path.dirname(self.recovery_file_path))
        except OSError:
            logging.warning("Cannot delete the recovery directory '%s'", self.recovery_file_path)
        self.show_timed_stats()

    def check_all(self):
        """
        To check for errors before waiting for example ten minutes for the decompression to complete
        """
        if not self.filelist_crawl_enabled:
            for rootdir in self.rootdirs:
                if not os.path.isdir(rootdir):
                    logging.warning("The passed in file is not a directory '%s'", rootdir)
        else:
            for rootdir in self.rootdirs[:]:
                if os.path.exists(rootdir):
                    if os.path.isdir(rootdir):
                        logging.warning("Passed file '%s' is directory. Skipping.", rootdir)
                        self.rootdirs.remove(rootdir)
                    else:
                        try:
                            with open(rootdir, 'rb') as _:
                                pass
                        except IOError:
                            logging.error("Passed file '%s' don't have permission to read", rootdir)
                            self.rootdirs.remove(rootdir)
                else:
                    logging.warning("Passed file '%s' does not exists. Skipping.", rootdir)
                    self.rootdirs.remove(rootdir)
            if not self.rootdirs:
                print 'List of files to be crawl is empty. Exiting.'
                logging.error('List of files to be crawl is empty. Exiting.')
                sys.exit(0)

        if self.options.symscan:
            # and not (self.options.symscan_defs and self.options.detected_files):
            if not self.options.symscan_defs:
                err_msg = "To use symscan you must provide a location for definitions"
                logging.error(err_msg)
                print err_msg
                sys.exit(1)
            if not self.options.detected_files:
                err_msg = "To use symscan you must provide a location to store any detected files."
                logging.error(err_msg)
                print err_msg
                sys.exit(1)
            if not os.path.exists(self.options.symscan_defs):
                err_msg = "The symscan defs does not exist '%s'" % self.options.symscan_defs
                logging.error(err_msg)
                print err_msg
                sys.exit(1)
            if not os.path.exists(self.options.symscan):
                err_msg = "The symscan executable does not exist '%s'" % self.options.symscan
                logging.error(err_msg)
                print err_msg
                sys.exit(1)

        if int(self.options.file_chunks) == 0:
            err_msg = "File chunk size cannot be zero"
            logging.error(err_msg)
            print err_msg
            sys.exit(1)

        if self.options.decomp:
            tempdir = self.decomp_temp_dir.uni_path
            logging.debug("tempdir = %s", tempdir)
            if not os.path.isdir(tempdir):
                try:
                    os.makedirs(tempdir)
                except OSError:
                    logging.fatal("Cannot create temp folder; exiting.")
                    print "Cannot create temp folder; exiting ..."
                    sys.exit(1)
            else:
                if os.listdir(tempdir) != [] and not self.options.recovery_point:
                    err_msg = "The temp folder is not empty at the start. " \
                              "Please pass in a recovery point or delete temp folder files. %s Exiting." % tempdir
                    logging.error(err_msg)
                    print err_msg
                    sys.exit(1)
        if self.options.symscan and not (self.options.symscan_defs and self.options.detected_files):
            err_msg = "To use symscan you must provide a location for definitions and " \
                      "also a location to store any detected files."
            logging.error(err_msg)
            print err_msg
            sys.exit(1)
        if not self.filelist_crawl_enabled:
            for rd in self.rootdirs:
                if not os.listdir(rd):
                    logging.warning("The directory to crawl is empty %s", rd)
        if not os.path.isdir(self.options.output) and not self.options.one_csv:
            if len(self.options.output) > 239:
                msg = ("The file path for the output is too long, you must shorten it. "
                       "The outputted files will be unreadable by nearly every system (%d) %s\nCrawler will now exit " %
                       (len(self.options.output), self.options.output))
                logging.error(msg)
                print msg
                sys.exit(1)

    def show_timed_stats(self):
        """
        Show how long each part
        """
        if self.options.time:
            end = time.time()
            elapsed = end-self.start
            logging.info("Total Time elapsed: %s", elapsed)
            print "Total Time elapsed: %s" % elapsed
            msg = ""
            for name in self.timers:
                msg = msg + "\n" + self.timers[name].show_time()
            logging.info(msg)
            print msg


def get_default_args(rootdirs,
                     ouptut_dir,
                     symscan,
                     symscan_defs):
    default = ['--eall',
               '--onecsv',
               os.path.join(ouptut_dir, 'one_csv.csv'),
               '--verbose',
               '-r', os.path.join(ouptut_dir, 'md5'),
               '-H', os.path.join(ouptut_dir, 'json'),
               '-o', os.path.join(ouptut_dir, 'out'),
               '-t',
               '-L', os.path.join(ouptut_dir, 'log.txt'),
               '-d', os.path.join(ouptut_dir, 'decompress'),
               '--symscan', symscan,
               '--symscan_defs', symscan_defs,
               '--detected_files', os.path.join(ouptut_dir, 'detected')]
    default.extend(rootdirs)
    return default


def main_nologs(args):
    (opts, rootdirs) = parseOpts(args, __version__)
    crawler = CrawlMaster(rootdirs, opts)
    crawler.crawl()


def main(args):
    (opts, rootdirs) = parseOpts(args, __version__)
    handlers = set_logging(opts)
    if opts.microMalHeurHash:
        logging.warning(
            "The -l option for extracting microMalHeurHash is DEPRECATED since 12/02/2013 DO NOT USE THE -l argument")
    logging.info("Crawler version: %s", __version__ )
    logging.info("Crawler started at: %s", time.asctime())
    logging.info("Command used:\n %s ", " ".join(sys.argv))
    logging.debug("json config:\n%s\n", getJSONOfOpt((opts, rootdirs)))
    crawler = CrawlMaster(rootdirs, opts)
    crawler.crawl()
    for handler in handlers:
        handler.close()
        logger = logging.getLogger()
        logger.removeHandler(handler)

if __name__ == "__main__":
    main(sys.argv)
