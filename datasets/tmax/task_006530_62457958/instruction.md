You are acting as a configuration manager tracking changes across a system. We have received a batch of legacy configuration files that need to be processed, converted, and safely archived into our central configuration repository.

Here is your task:

1. **Extract and Convert**: 
   There is a tarball located at `/home/user/legacy_configs.tar.gz` containing several `.conf` files. These files are unfortunately encoded in `ISO-8859-1`.
   Extract them, convert their character encoding to `UTF-8`, and save the converted files into a new directory: `/home/user/converted_configs/`.

2. **Safe Archiving**:
   You must write and execute a Python script to add these converted `UTF-8` `.conf` files into our master configuration archive, located at `/home/user/master_configs.zip`. 
   Because this master archive might be accessed concurrently by other services, your Python script **must** acquire an exclusive file lock on a lockfile named `/home/user/master.lock` before opening or modifying the zip file, and release the lock after closing the zip file. Use Python's `fcntl.flock` for this locking mechanism.

3. **Link Management**:
   Create a new directory `/home/user/latest_configs/`. Inside this directory, create symbolic links to each of the converted `.conf` files in `/home/user/converted_configs/`. The symlinks must have the exact same names as the `.conf` files.

Ensure all steps are complete and the Python script you write is saved as `/home/user/update_configs.py`.