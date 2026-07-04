You are a backup administrator tasked with archiving a specific set of critical data directories based on an automated system's multi-line log output.

You have been provided with a multi-line log file at `/home/user/backup_queue.log`. This file contains the queue of backup jobs. The format of the log contains records that look exactly like this:

```
BEGIN_JOB
JobID: 1045
Priority: HIGH
Status: REQUIRED
Path: /home/user/data/app_config
END_JOB
```

Some jobs will have a `Status:` of `IGNORED` or `COMPLETED`. 

Your task is to:
1. Write a C program at `/home/user/queue_parser.c` that reads `/home/user/backup_queue.log`.
2. The program must parse the multi-line records and extract the `Path:` value ONLY for jobs where the `Status:` is exactly `REQUIRED`.
3. The program must write these extracted absolute paths to a flat text file at `/home/user/targets.txt`, with one path per line.
4. Compile your C program and run it to generate `/home/user/targets.txt`.
5. Use the `tar` command to create a gzip-compressed archive at `/home/user/required_backups.tar.gz` containing all the directories (and their contents) listed in `/home/user/targets.txt`.

Ensure your C program handles the multi-line parsing correctly (the order of `Priority`, `Status`, and `Path` within a `BEGIN_JOB`/`END_JOB` block might vary, but they will always be on separate lines within the block).

Do not include any directories in the archive that are not marked as `REQUIRED`.