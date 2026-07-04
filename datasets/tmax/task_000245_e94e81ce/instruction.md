I need a Python script to act as a configuration manager that tracks changes between a live directory and a baseline backup archive. 

Please create a Python script at `/home/user/sync_configs.py` that performs the following steps when executed:

1. **Archive Integrity & Extraction**: Validate that the baseline archive at `/home/user/base_config.tar.gz` is a valid gzip-compressed tarball. If it is corrupt or invalid, the script should exit with status code 1.
2. **Change Detection**: Compare the contents of the baseline archive against the live configuration directory at `/home/user/live_config/`. 
3. **Text Transformation**: For any `.conf` file in the live directory that has different contents than its counterpart in the baseline archive, OR is completely new (does not exist in the archive), modify the live file in `/home/user/live_config/` by exactly prepending the following line to the top of the file:
   `# TRACKED CHANGE`
   (Note: Ensure there is a newline character after this header). Files that are identical to the baseline should remain completely untouched.
4. **Archive Creation**: Create a new gzip-compressed tar archive at `/home/user/tracked_config.tar.gz` that contains all the files from the newly updated `/home/user/live_config/` directory.

You can use standard Python libraries (like `tarfile`, `filecmp`, `os`, `shutil`) or call out to shell utilities (like `sed` or `tar`) via `subprocess` within your Python script. 

Once you have created the script, please run it so I can verify the results.