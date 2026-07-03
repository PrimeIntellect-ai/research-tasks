You are acting as a configuration manager for a legacy Linux environment. You need to create a custom backup utility to track changes in our application configuration directories.

We have a configuration directory located at `/home/user/app_configs`. Unfortunately, some legacy applications have created circular symbolic links within these directories, which causes standard backup scripts (like `tar -h`) to fall into infinite loops. Additionally, some configuration files (like large generated routing tables) are very large and need to be chunked.

Your task is to write a Bash script at `/home/user/safe_archive.sh` and execute it to produce the final backup. The script must perform the following:

1. **Recursive Traversal with Cycle Detection**: Traverse `/home/user/app_configs` and follow all symbolic links. You must implement a mechanism to detect and skip circular symbolic links (e.g., by tracking visited directories) so the script does not loop infinitely.
2. **File Splitting**: For every regular file encountered during the traversal:
   - If the file is 1MB (1048576 bytes) or larger, split it into 1MB chunks. Name the chunks with the original filename followed by `.part_aa`, `.part_ab`, etc. (Standard `split` command behavior).
   - If the file is smaller than 1MB, keep it as is.
3. **Custom Compression**: Collect all the resulting files (and chunks) into a flat staging directory (do not preserve the original directory structure). Create a `tar` archive of these files, compress it with `gzip`, and finally encode the gzipped file using `base64`. 
4. **Outputs**:
   - Save the final encoded backup to `/home/user/config_backup.tar.gz.b64`.
   - Create a log file at `/home/user/archive_log.txt` containing the base names of all files and chunk files that were included in the final archive. The list must be sorted alphabetically, one filename per line.

Ensure your script handles the traversal gracefully, and execute it to generate the final backup and log file.