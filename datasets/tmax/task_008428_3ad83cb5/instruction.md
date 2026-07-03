You are acting as a configuration manager tracking changes in a Linux environment. A recent system update modified several configuration files, and you need to parse the update log, verify the files, create a manifest, and package them using a custom backup format.

Your task is to perform the following steps using Bash:
1. Read the multi-line log file located at `/home/user/update.log`. This log contains multiple update records. Each record has a `Files:` section followed by a list of file paths.
2. Extract all the file paths listed under the `Files:` sections.
3. Filter these file paths based on the following metadata criteria. Keep ONLY the files that:
   - Actually exist on the filesystem.
   - Are located within `/home/user/etc/` or its subdirectories.
   - Have a size strictly less than 100 KB.
   - Have either a `.conf` or `.yaml` file extension.
4. Generate a manifest file at `/home/user/manifest.txt` containing the SHA-256 checksums of the files that passed the filter. The format should be exactly the output of the `sha256sum` command (e.g., `<checksum>  /home/user/etc/...`). Sort the manifest alphabetically by file path.
5. Package the filtered configuration files AND the `/home/user/manifest.txt` file into a custom compressed format. The custom format requires you to:
   - Create a single `tar` archive containing the exact absolute paths of the filtered files and the manifest.
   - Compress the tar archive using `gzip`.
   - Encode the resulting gzipped file using `base64`.
6. Save the final base64-encoded string to a file at `/home/user/backup.cpack`.

Ensure all file paths in the tar archive and manifest are absolute paths.