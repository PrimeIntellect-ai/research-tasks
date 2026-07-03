As a backup administrator, you are tasked with archiving application data using a proprietary, vendored Python archiving tool called `py-archiver`. 

You have been provided with the source code for this tool at `/app/py-archiver-1.0.0`. However, the tool is currently buggy and highly unoptimized. Before you can use it to back up the active data in `/home/user/app_data` to `/home/user/archives`, you must fix the source code.

Your objectives:
1. **Fix Recursive Traversal**: The tool currently only reads the top-level directory. Modify it to recursively traverse all subdirectories.
2. **Optimize File Chunking**: The tool's file splitting mechanism is currently reading files 1 byte at a time, making it impossibly slow. Fix the buffer size to something reasonable (e.g., 1MB) for reading and splitting operations.
3. **Implement File Locking**: The files in `/home/user/app_data` are actively being written to by other processes. Implement shared file locking (e.g., using `fcntl.flock` with `LOCK_SH`) during the read operations in the archiver to prevent archiving partially written states.

Once you have fixed `/app/py-archiver-1.0.0` (you can install it in editable mode or just run it directly), execute it to archive `/home/user/app_data` into `/home/user/archives`. The tool accepts arguments like so:
`python -m pyarchiver.cli --source /home/user/app_data --dest /home/user/archives --chunk-size 5MB`

An automated test will evaluate the performance of your fixed archiver package by running it against a large synthetic dataset and measuring the execution time. Ensure your fixes are correctly implemented in the vendored package.