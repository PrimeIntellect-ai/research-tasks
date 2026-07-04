You are tasked with building a configuration management archiving tool. We are managing configurations for a simulated system root located at `/home/user/sys_root`.

Your objective is to extract specific target directories, perform a large-scale text migration on the configurations, and write a C utility that generates a cryptographically sound manifest and archive.

**Phase 1: Path Manipulation and Staging**
1. Read the configuration file located at `/home/user/backup_targets.ini`. It contains a list of paths relative to `/home/user/sys_root`.
2. Create a staging directory at `/home/user/staging`.
3. Copy all files and directories listed in the `.ini` file from `/home/user/sys_root` into `/home/user/staging`, preserving their directory structure (e.g., a target of `etc/app1` should end up at `/home/user/staging/etc/app1`). 

**Phase 2: Configuration Migration (Large-scale text editing)**
Our systems are migrating to a new network daemon. Across all `.conf` files in the staging directory, you must replace all instances of the configuration key `server_ip=` with `bind_addr=`. The values assigned to the keys must remain unchanged. This must only be applied to the files in `/home/user/staging`, leaving the original `sys_root` intact.

**Phase 3: Manifest and Checksum Generation (C Programming)**
Write a C program named `/home/user/config_archiver.c` and compile it to `/home/user/config_archiver`. The C program must:
1. Accept exactly one command-line argument: the path to the staging directory (`/home/user/staging`).
2. Recursively traverse the directory to find all files ending in `.conf`.
3. For each file, compute its SHA-256 checksum using OpenSSL (`libcrypto`).
4. Write a manifest file to `/home/user/manifest.txt` where each line is formatted exactly as:
   `<SHA256_HEX> <relative_path_from_staging_root>`
   *(Example: `a1b2c3... etc/app1/settings.conf`)*
   Sort the lines in the manifest alphabetically by the relative path.
5. After generating the manifest, the C program must programmatically invoke a shell command to compress the contents of the staging directory into `/home/user/config_backup.tar.gz`. Ensure the tarball is created such that extracting it yields the relative directories directly (i.e., it should not contain the `staging` wrapper directory).

**Constraints:**
* Use C for the manifest generator (shell/Python/etc. can be used for Phase 1 & 2).
* Ensure your C program handles files securely and closes file handles properly. You may need to link against `crypto`.
* Do not modify the original `/home/user/sys_root`.