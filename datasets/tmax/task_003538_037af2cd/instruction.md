You are acting as a backup administrator. We need to securely archive a set of configuration files, but we must sanitize them first to prevent leaking secrets. 

You have been given a directory located at `/home/user/server_configs`. Inside this directory (and its subdirectories), there are several configuration files ending in `.conf`. 

Your task is to:
1. Traverse the `/home/user/server_configs` directory recursively to find all `.conf` files.
2. Edit these files in place using Python to redact sensitive keys. Specifically, find any line containing `SECRET_KEY=<alphanumeric_string>` and replace the alphanumeric string with `REDACTED`. For example, `SECRET_KEY=aB39xQ` should become `SECRET_KEY=REDACTED`.
3. After sanitizing the files, generate a SHA256 checksum manifest of all the `.conf` files. Save this manifest to `/home/user/manifest.sha256`. The format of each line should be `[SHA256_HASH]  [relative_path_from_server_configs]` (e.g., `e3b0c442...  app1/settings.conf`).
4. Create a gzip-compressed tar archive of the sanitized `.conf` files at `/home/user/config_backup.tar.gz`. The archive should maintain the internal directory structure relative to `/home/user/server_configs` (i.e., extracting it should yield `app1/settings.conf`, not `home/user/server_configs/app1/settings.conf`).
5. Verify the integrity of the created archive to ensure it is a valid gzip tarball (you can do this via standard shell commands, just ensure the final archive is perfectly valid and not corrupted).

Do not include any files other than `.conf` files in the manifest or the tarball.