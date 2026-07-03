You are tasked with fixing a custom configuration archiving tool written in C. 

The tool, located at `/home/user/config_archiver.c`, is designed to traverse a directory, read configuration files and Write-Ahead Logs (WALs) using streaming I/O, apply a custom Run-Length Encoding (RLE) compression algorithm, and write the output to an archive file.

However, the configuration manager recently created a cyclic symlink in the `/home/user/configs` directory. Because the archiver uses `stat()` instead of `lstat()` and doesn't track visited inodes, it follows symlinks and gets trapped in an infinite loop, eventually crashing or exhausting disk space.

Your tasks:
1. Modify `/home/user/config_archiver.c` to properly detect and **skip** symlinks completely. Do not archive symlinks, and do not recurse into them. You must use `lstat()` to detect if a file is a symlink.
2. Compile your modified C program using `gcc /home/user/config_archiver.c -o /home/user/archiver`.
3. Run the compiled program: `/home/user/archiver /home/user/configs /home/user/backup.rle`.
4. Ensure the archive `/home/user/backup.rle` is successfully created.
5. **DO NOT** delete, modify, or unlink the symlinks in `/home/user/configs`. Your C code must be robust enough to handle their presence.

The automated verification will check if `/home/user/backup.rle` contains the correctly compressed data from the regular files, and that the cyclic symlink still exists in the original directory.