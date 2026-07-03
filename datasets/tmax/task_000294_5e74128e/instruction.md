I am a technical writer trying to organize an old documentation repository, but the backup files I received are a mess. The previous automated backup script followed symbolic links into infinite loops, crashing and creating a deeply nested, corrupted archive structure. 

I need you to process the master archive, extract the useful documentation while avoiding the symlink traps, parse the backup logs to identify the exact error incident, and package everything cleanly.

The master archive is located at `/home/user/raw_data.tar`.

Please perform the following steps:
1. Extract `/home/user/raw_data.tar`. Inside, you will find a configuration file (`rules.ini`), a multi-line log file (`backup.log`), and several nested archives (`docs_a.tar.gz`, `docs_b.tar.gz`, etc.).
2. Read `rules.ini`. It specifies the valid documentation file extensions and the file format of a specific documentation build tool hidden in the archives.
3. Parse the `backup.log` file. This log contains multi-line error traces. Find the multi-line error block that specifically crashes with an `InfiniteSymlinkException`. Extract the numeric `Incident ID` associated with this specific error and write just the number to `/home/user/incident_id.txt`.
4. Safely extract the nested documentation archives (`docs_a.tar.gz`, etc.). *Warning:* These archives contain infinite symlink loops. You must extract them in a way that safely ignores or removes all symbolic links to prevent recursive loops.
5. Create a clean directory at `/home/user/clean_docs/`.
6. Search the extracted contents (ignoring symlinks) and copy all files that match the valid extensions specified in `rules.ini` directly into `/home/user/clean_docs/` (flatten the directory structure so all files are at the root of `clean_docs`).
7. There is exactly one file among the extracted contents that is an executable binary matching the "Tools format" specified in `rules.ini` (e.g., an ELF executable). Identify this file and copy it to `/home/user/clean_docs/build_tool`.
8. Finally, create a new archive at `/home/user/organized_docs.tar.gz` containing all the files inside `/home/user/clean_docs/`. The files must be at the root of the archive (do not include the `clean_docs` parent directory folder itself in the archive).

Ensure that all file operations are completed successfully and that the final `.tar.gz` is well-formed.