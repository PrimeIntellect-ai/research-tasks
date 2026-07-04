You are tasked with acting as a configuration manager handling a legacy system migration. 

In the `/home/user/environments` directory, there is a complex directory structure containing several compressed backup files (`.zip`). These archives contain various configuration files (`.conf`).

Your task is to:
1. Recursively traverse the `/home/user/environments` directory to find all `.zip` files.
2. Extract these archives to access the `.conf` files within them. Note that some archives may contain nested directories.
3. Perform a mass configuration update: Search through all extracted `.conf` files and replace every instance of the string `db_host=old-db.legacy.local` with `db_host=new-cluster.modern.local`. 
4. Ensure your updates are written safely (e.g., using temporary files and atomic moves, or robust in-place editing tools).
5. Once all `.conf` files have been updated, collect ALL the modified `.conf` files (flatten the directory structure, so just the files themselves) and archive them together into a new, multi-part tarball archive.
6. The final archive must be named `updated_configs.tar.gz` and split into chunks of exactly 500 bytes.
7. Save the split archive chunks in `/home/user/final_backup/` with the standard `split` suffix format (e.g., `updated_configs.tar.gz.aa`, `updated_configs.tar.gz.ab`, etc.). 

Requirements:
- The `/home/user/final_backup/` directory must be created if it does not exist.
- Do not include the original `.zip` files or any unaltered files in the final backup.
- Do not preserve the original folder paths of the `.conf` files inside the final tarball; the tarball should just contain the flat list of `.conf` files at its root.

Let me know when you have successfully completed these operations.