You are acting as a backup administrator for our team. We have a directory of raw, poorly-named data files that need to be cleaned up, verified, and safely archived. 

Write and execute a Bash script at `/home/user/backup_manager.sh` that performs the following steps automatically:

1. Target directory: `/home/user/raw_data`
2. **Bulk File Renaming**: Inside the target directory, find all files and rename them according to these rules:
   - Replace any spaces in the filenames with underscores (`_`).
   - Convert all file extensions to strictly lowercase (e.g., `.CSV` becomes `.csv`, `.Txt` becomes `.txt`). Keep the base filename's case intact, only change the extension and spaces.
3. **Manifest and Checksum Generation**: After renaming, generate a SHA-256 manifest of all files in the directory. Save this manifest to `/home/user/manifest.sha256`. The format should be the standard `sha256sum` output (`<hash>  <filepath>`).
4. **Archiving**: Create a gzip-compressed tarball of the `/home/user/raw_data` directory (including the directory itself) at `/home/user/archive.tar.gz`.
5. **Stream Redirection & Logging**: Calculate the SHA-256 checksum of the final `archive.tar.gz` file. Then, count the total number of files that were archived. Write these two pieces of information to `/home/user/backup_log.txt` in exactly this format:
   ```
   Archive Checksum: <sha256_hash_of_archive.tar.gz>
   Files Archived: <number_of_files>
   ```

After writing the script, you must run it so the final artifacts (`manifest.sha256`, `archive.tar.gz`, and `backup_log.txt`) are generated.