You are a backup administrator tasked with writing a custom incremental backup tool. 

The source directory is `/home/user/data_source`.
The destination directory is `/home/user/backup_dest` (create this directory if it doesn't exist).
The timestamp reference file is `/home/user/last_backup.ts`.

Write a script in any language (Python, Bash, etc.) to perform an incremental backup with the following rules:
1. Traverse `/home/user/data_source` recursively.
2. For regular files: If the file is newer than `/home/user/last_backup.ts` (based on modification time), copy it to `/home/user/backup_dest`, maintaining the exact relative directory structure.
3. For hard links: If multiple files in the source directory point to the same inode and are being backed up in this run, they must share the same inode in the destination directory (i.e., preserve the hard link relationship).
4. For symbolic links: Always copy the symbolic link itself to the destination (do not follow it to copy the target), regardless of its modification time. Preserve its original target path.
5. Do not copy directories themselves unless they contain a file/link that needs to be backed up.

After performing the backup, your script must generate a log file at `/home/user/backup_log.txt` containing a record of every file or link created in the destination. The log file must be sorted alphabetically by the relative path, with one entry per line in the following format:
`[TYPE] relative/path/to/item`

Where `[TYPE]` is one of:
- `[FILE]` for a regular file (the first time an inode is copied)
- `[HLINK]` for a hard link (subsequent files sharing an already-copied inode)
- `[SLINK]` for a symbolic link

Example log entry:
`[FILE] docs/report.txt`
`[HLINK] docs/report_backup.txt`
`[SLINK] shortcuts/report.txt`

Execute your script so the backup and the log file are fully generated.