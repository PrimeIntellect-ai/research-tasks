You are tasked with building a tool for a configuration management system to perform secure incremental backups based on a change log.

We track configuration changes in a multi-line log file located at `/home/user/config_log.txt`. 

Your goal is to write a C program at `/home/user/archiver.c` (and compile it to `/home/user/archiver`) that does the following:
1. Parses the multi-line log file `/home/user/config_log.txt`.
2. Identifies the *last* (most recent, at the bottom of the file) configuration update block.
3. Extracts the list of modified configuration files from that block.
4. For each modified file (which will be located in `/home/user/configs/`), computes its SHA256 checksum. You may invoke shell commands like `sha256sum` from within your C code if desired.
5. Writes a manifest of these checksums to `/home/user/manifest.txt`. The format must be exactly what `sha256sum` outputs: `<hash>  <filename>` (where filename is just the basename of the file).
6. **Important Constraint:** The write to the manifest must be atomic. Your C program *must* write the output to a temporary file (`/home/user/manifest.txt.tmp`) first, and then use the C `rename()` function to replace `/home/user/manifest.txt`.
7. Finally, after the manifest is successfully created, package *only* those updated files into a gzip-compressed tarball at `/home/user/incremental.tar.gz`. You can do this step via standard shell commands after your C program runs, or within the C program itself.

The log file `/home/user/config_log.txt` format looks like this:
```
[UPDATE]
Date: 2023-10-01
Author: admin
Modified:
 - network.conf
 - database.conf
[END]

[UPDATE]
Date: 2023-10-05
Author: dbadmin
Modified:
 - database.conf
 - cache.conf
[END]
```

In this example, the most recent update modified `database.conf` and `cache.conf`. You should only back up and hash those two files.

Ensure your compiled program runs successfully and leaves the system with the atomic `/home/user/manifest.txt` and the archive `/home/user/incremental.tar.gz` containing the files at the root of the tar archive (do not include the `configs/` directory structure in the tarball, just the files themselves).