You are a developer tasked with organizing and recovering legacy project files received from an overseas contractor. The contractor sent the files using an eccentric, proprietary custom compression format, and the transfer was notoriously unreliable, so some files might be corrupted. 

Your goal is to extract, verify, convert, and safely repackage these files.

Here are the specifics of your task:

1. **Locate the incoming archive**: The contractor has uploaded the file to `/home/user/incoming/project.cgar`.
2. **Decompress the custom archive**: The `.cgar` (Custom Gzip And Reverse) format is created through the following pipeline: 
   - Files are packed into a `tar` archive.
   - The archive is compressed using `gzip`.
   - The compressed binary is encoded in `base64`.
   - Finally, every line of the base64 output is reversed (e.g., using the `rev` command).
   You must reverse this process to extract the contents into `/home/user/extracted/`.
3. **Verify Archive Integrity**: Inside the extracted contents, you will find a `source_files.tar` archive and a `checksums.md5` file. Extract `source_files.tar` into a subdirectory named `/home/user/extracted/source/`. 
   Use the `checksums.md5` file to verify the integrity of the extracted source files. The transfer was faulty, so at least one file is corrupted. You must permanently delete any file in the `source/` directory that fails the MD5 checksum verification.
4. **Character Encoding Conversion**: The remaining valid files in the `source/` directory are plain text source files, but they were saved using the `WINDOWS-1251` character encoding. You must convert all the surviving files to `UTF-8` encoding. Overwrite the files or save the converted files such that only the UTF-8 versions remain.
5. **Organize and Repackage**: 
   - Move all the verified, UTF-8 encoded files into a new directory: `/home/user/clean_source/`.
   - Finally, you must package the entire `clean_source` directory (so that the archive extracts a `clean_source/` folder containing the files) into a new archive located at `/home/user/clean_project.cgar`. 
   - This new archive **must** be created using the exact same `.cgar` custom compression pipeline described in step 2 (tar -> gzip -> base64 -> rev).

Ensure that all tools you use are standard Linux utilities available in Bash. Do not leave any original or corrupted files in the `clean_source` directory.