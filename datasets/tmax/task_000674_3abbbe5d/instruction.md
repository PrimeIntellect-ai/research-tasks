You are a Database Reliability Engineer responding to a catastrophic metadata loss. Our backup metadata database was corrupted, but we have a screen recording of the legacy monitoring dashboard saved at `/app/backup_monitor.mp4`. 

Your task is to recover the backup statuses from this video, reconstruct a SQLite database, and write an analysis tool.

1. **Recover Data from Video**: 
   The video `/app/backup_monitor.mp4` runs at 1 frame per second. Each frame corresponds to a sequential backup event, starting at UNIX timestamp `1700000000` for the first frame, incrementing by 1 second per frame.
   Analyze the video: if a frame's average grayscale pixel intensity is greater than 128, the backup was a success (`status = 1`). If it is less than or equal to 128, the backup failed (`status = 0`).

2. **Reconstruct Database**:
   Create a SQLite database at `/home/user/recovered_backups.db` with a table:
   `CREATE TABLE backups (timestamp INTEGER PRIMARY KEY, status INTEGER);`
   Insert the recovered data into this table.

3. **Create Analysis Tool**:
   Write a Python script at `/home/user/backup_analyzer.py` that accepts a single integer argument representing a UNIX timestamp `T`. 
   The script must connect to `/home/user/recovered_backups.db` and use a parameterized query with **SQL Window Functions** to calculate the length of the *longest streak of consecutive failed backups* (status = 0) that occurred strictly before timestamp `T`.
   The script should print ONLY the integer length of this maximum streak to `stdout`.

Ensure `/home/user/backup_analyzer.py` is executable. Automated tests will verify your script against a reference implementation using hundreds of random timestamps.