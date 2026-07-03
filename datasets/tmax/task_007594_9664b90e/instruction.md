You are an AI assistant helping a technical writer organize a complex documentation repository. 

Our documentation build system has been failing because a previous backup script created infinite symlink loops. I have an archive of the raw documentation files, a configuration file specifying the intended layout, and a log file from the failed build system.

Here is your task:
1. Extract the nested archive located at `/home/user/raw_docs.tar.gz`. Inside it, you will find two secondary archives: `core.tar.gz` and `api.zip`. Extract these into `/home/user/extracted_docs/`.
2. Analyze the multi-line log file at `/home/user/build_errors.log`. This log contains error blocks separated by `---`. Find all files that failed specifically with the reason `Error: Infinite Symlink Loop`. 
3. Read the configuration file `/home/user/docs_config.ini`. This INI file maps source file names (which exist somewhere in the extracted archives) to their intended destination paths in `/home/user/public_docs/`.
4. Write and execute a Python script `/home/user/organize_docs.py` that recreates the documentation tree in `/home/user/public_docs/` by creating symbolic links to the extracted source files. 
   - **Important constraint:** Do NOT create symlinks for any source file that was identified in `build_errors.log` as causing an `Infinite Symlink Loop`.
   - The symlinks must point to the absolute paths of the files in `/home/user/extracted_docs/`.
5. Finally, generate a text file at `/home/user/success_manifest.txt` containing the absolute paths of all successfully created symlinks in `/home/user/public_docs/`, sorted alphabetically, one per line.

Requirements:
- Ensure the destination directory `/home/user/public_docs/` is created before linking.
- Ensure your script correctly handles the multi-line format of the log file.