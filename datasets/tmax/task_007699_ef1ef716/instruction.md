You are an artifact manager responsible for curating a local repository of binary packages and their metadata. 

In the directory `/home/user/artifacts/`, there are several metadata files (ending in `.meta`). These files contain key-value pairs describing binary artifacts (e.g., `architecture: x86_64`, `status: pending`).

Due to multiple background systems indexing this repository, you must ensure thread-safe and process-safe modifications.

Your task is to write a Python script and perform an incremental backup by following these steps:

1. Create a Python script at `/home/user/curate.py` that iterates over all `.meta` files in `/home/user/artifacts/`.
2. For each file, the script must:
   - Open the file and acquire an exclusive lock using the `fcntl.flock` method.
   - Parse the text content.
   - If the file contains exactly `architecture: x86_64` and `status: pending`, update the status line to `status: curated`. Leave all other lines and files untouched.
   - Write the modified contents back to the file.
   - Release the lock and close the file.
3. Execute the script to update the metadata files.
4. After updating the files, create an incremental backup of the `/home/user/artifacts/` directory. A full backup and a snapshot file already exist. You must use the existing snapshot file `/home/user/snapshot.snar` to create a new incremental backup archive at `/home/user/backup_inc.tar` using the `tar` command. 

Ensure that your incremental tarball only captures the files that were modified by your Python script.