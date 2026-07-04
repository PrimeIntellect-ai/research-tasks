You are managing a system that tracks configuration changes. A service periodically dumps raw configuration files into `/home/user/configs/raw/`. Some of these files are corrupted or incomplete due to race conditions during writing.

You need to write a Python script at `/home/user/config_archiver.py` that processes these files and archives the valid ones. 

Here are the requirements for your script:
1. Scan the directory `/home/user/configs/raw/`. Process only files that have exactly `644` permissions (metadata-based filtering).
2. Validate each processed file. A valid configuration file starts with a specific 4-byte binary magic header: `\xCF\xFA\xED\xFE`. 
3. Immediately following the 4-byte binary header is UTF-8 encoded text. The first line of this text will always be `VERSION: <integer>` (e.g., `VERSION: 42`).
4. For all *valid* configuration files found, add them to a new compressed archive at `/home/user/configs/archive/active_configs.tar.gz`. The files in the tar archive should not contain their full path (store them at the root of the archive).
5. Create a symbolic link at `/home/user/configs/latest.tar.gz` that points to `/home/user/configs/archive/active_configs.tar.gz`.
6. Identify the single valid raw configuration file with the highest `VERSION` number. Create a hard link at `/home/user/configs/latest_valid_raw.cfg` pointing to this specific raw file.

Once your script is written, run it so the archive and links are created. Do not remove or modify the original files in `/home/user/configs/raw/`.