You are tasked with organizing and securely backing up a developer's rapidly changing project workspace. The project contains a mix of large binary and text files that are constantly being written to by active background services. You must implement an efficient, incremental backup system.

Your requirements are as follows:

1. **Fix and Install the Diffing Tool**:
   We have vendored the `bsdiff4-1.2.4` package at `/app/bsdiff4-1.2.4/`. It is required for creating efficient binary patches. However, it currently fails to install due to a deliberate misconfiguration in its build script. Find the issue in its `setup.py` or build files, fix it, and install the package into your Python environment.

2. **Implement an Incremental Backup Script**:
   Write a Python script at `/home/user/backup.py` that backs up the contents of `/home/user/project/` to `/home/user/backup_dir/`.
   - If a file exists in `/home/user/project/` but not in `/home/user/backup_dir/`, copy it over exactly.
   - If a file exists in both, calculate the binary delta (patch) from the file in `backup_dir` to the file in `project` using the `bsdiff4` library. Save this patch in `/home/user/backup_dir/` as `<filename>.patch` (and leave the older full file intact for future reference). Do NOT copy the new full file over; we only want the patch.
   
3. **Handle Concurrent Access**:
   Background processes are constantly appending to the log and data files in `/home/user/project/`. When reading files from `/home/user/project/` in your Python script, you MUST acquire a shared file lock using `fcntl.flock(fd, fcntl.LOCK_SH)` before reading, and release it (`fcntl.LOCK_UN`) after reading. This ensures you do not read a file while it is in the middle of a blocked write.

4. **Run the Backup**:
   Execute your script so that `/home/user/backup_dir/` is fully populated with the base files and `.patch` files representing the latest state of `/home/user/project/`. 

To succeed, your backup approach must be highly storage-efficient. An automated verifier will measure the total size in bytes of the newly created files in `/home/user/backup_dir/`. If you just copy files instead of creating patches, you will fail the storage efficiency threshold.