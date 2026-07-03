You are acting as a storage administrator managing disk space and backups for a server. 

An automated backup script has been failing because it follows symlinks and gets stuck in an infinite directory loop. Your task is to fix the directory structure, log the culprit, and perform the backup manually.

Here are your instructions:
1. Read the configuration file located at `/home/user/backup.conf`. It is in standard INI format. Under the `[Backup]` section, you will find `source_dir` and `dest_archive` keys.
2. The `source_dir` contains a nested symlink that points back to an ancestor directory, creating an infinite loop. Identify this symlink and delete it.
3. Write the absolute path of the symlink you deleted to a file named `/home/user/loop_symlink.txt`.
4. Once the infinite loop is removed, create a compressed gzip tar archive (`.tar.gz`) of the entire `source_dir`. Save this archive to the path specified by the `dest_archive` key in the configuration file.

Ensure that your final tarball contains the valid contents of the source directory and no infinite loops.