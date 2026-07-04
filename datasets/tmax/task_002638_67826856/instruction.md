As a configuration manager, you need to implement a robust script to update a master configuration archive. Our systems pull their state from a single binary archive file, and multiple background processes might try to update it simultaneously. 

Your task is to write a Python script at `/home/user/atomic_update.py` that securely updates a ZIP archive with new configuration files. 

The script must accept two arguments:
`python3 atomic_update.py <path_to_zip_archive> <path_to_incoming_dir>`

The script MUST follow these strict operational requirements:
1. **File Locking**: Before touching the archive, the script must acquire an exclusive system lock (`fcntl.LOCK_EX`) on a lockfile named `<path_to_zip_archive>.lock`.
2. **Atomic Writes**: To prevent a corrupted state if the system crashes during the update, the script must write the new updated archive to a temporary file first (using the `tempfile` module).
3. **Archive Merge**: The script must read the existing archive. It should copy all existing files to the new temporary archive. However, if a file in the `<path_to_incoming_dir>` has the exact same name as an existing file in the archive, the version from the incoming directory must be used instead (overwriting it). Any new files in the incoming directory that aren't in the archive must also be added. 
4. **Atomic Replacement**: Once the temporary ZIP is fully written and closed, use `os.replace()` to atomically swap the old archive with the new temporary file.
5. **Lock Release**: Finally, release the lock and close the lockfile.

Once you have written the script, execute it with the following arguments to perform the update:
`python3 /home/user/atomic_update.py /home/user/master_config.zip /home/user/incoming_configs`

Note: `/home/user/master_config.zip` and `/home/user/incoming_configs` already exist on the system.