You are acting as a backup administrator. The automated nightly backup for a critical data directory failed because the archiving script encountered infinite symbolic link loops. 

You have been provided with the following files:
1. `/home/user/backup_config.ini`: A configuration file specifying the backup parameters.
2. `/home/user/failed_backup.log`: A log file from the failed backup attempt containing multi-line error records.
3. `/home/user/backup_source`: The directory tree that needs to be backed up.

Your task is to write and execute a Python script (you may also use shell commands if helpful) to fix the backup process. You must:

1. Parse `/home/user/backup_config.ini` to determine the `source_dir`, the `output_file`, and the required action (`on_loop_detect`).
2. Parse the multi-line error blocks in `/home/user/failed_backup.log` to extract the absolute paths of the symbolic links that caused a "File system loop detected" error.
3. Apply the action specified in the config file to these offending symlinks (in this case, you will need to delete them). Do not delete any valid symlinks or files that did not cause loops.
4. Output the absolute paths of the deleted symbolic links to `/home/user/removed_links.txt`, with one path per line, sorted alphabetically.
5. Create a compressed tarball (`.tar.gz`) of the `source_dir` and save it to the location specified by `output_file` in the configuration. The archive should store remaining valid symlinks as symlinks (do not follow them/dereference them during archiving). The archive must contain the base directory itself (e.g., extracting it should create a `backup_source` folder).

Ensure your script handles the multi-line nature of the log file correctly, as the path and the error reason are on separate lines within each log record.