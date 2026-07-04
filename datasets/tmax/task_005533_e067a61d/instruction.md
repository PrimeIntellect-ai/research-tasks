You are managing system configurations and need to track changes and package a config update based on a symlink tree.

You have been provided with an archive of configurations at `/home/user/configs.tar` and a directory of symlinks at `/home/user/config_tree/`. Some of the symlinks in the tree are valid and point to expected files in the extracted configs, while others are broken.

Perform the following steps:
1. Extract `/home/user/configs.tar` into a new directory `/home/user/extracted_configs/`.
2. Write a C program at `/home/user/tracker.c` that acts as a configuration manager tracking changes. The program must:
   - Iterate through the files in `/home/user/config_tree/`.
   - Use path manipulation (e.g., `realpath`) to resolve the target of each symlink.
   - Ignore any broken symlinks.
   - For each valid symlink, compute the SHA256 checksum of its target file (you may use OpenSSL or shell out to `sha256sum`).
   - Perform a format conversion by writing the gathered metadata into a strict JSON file at `/home/user/manifest.json`. The JSON must be an array of objects, with each object formatted exactly like this:
     `{"link_name": "<name_of_symlink>", "target_path": "<absolute_path_of_target>", "sha256": "<checksum_of_target>"}`
3. Compile and run your C program to generate `/home/user/manifest.json`. Link against `crypto` if using OpenSSL (`-lcrypto`).
4. Create a final gzip-compressed tar archive at `/home/user/update.tar.gz` containing:
   - The generated `manifest.json` file.
   - Only the valid target `.conf` files that were successfully resolved, placed in an `extracted_configs/` directory within the archive.

Do not include any broken links or unreferenced config files in the final archive.