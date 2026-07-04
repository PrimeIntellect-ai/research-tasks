You are an automated backup operator testing restores for a secure storage system. We need to build a pipeline that automatically validates backup restores whenever a new restore snapshot is pushed to our central backup repository.

Please set up the following pipeline exactly as specified:

1. **Directories**:
   Create the following directories if they don't exist:
   - `/home/user/spool` (for queued jobs)
   - `/home/user/results` (for validation results)

2. **Git Backup Repository & Hook**:
   Initialize a bare Git repository at `/home/user/backup_repo.git`.
   Create a `post-receive` hook in this repository (`/home/user/backup_repo.git/hooks/post-receive`). The hook must:
   - Read from standard input to get the `oldrev`, `newrev`, and `refname`.
   - For each line read, extract the `newrev` (the commit hash).
   - Create a file in `/home/user/spool/` named exactly `<newrev>.job` containing the `<newrev>` string. Ensure the hook is executable.

3. **Validation Program (C++)**:
   Write a C++ program at `/home/user/verify_restore.cpp` and compile it to `/home/user/verify_restore`.
   The program must read a list of filenames from standard input (one filename per line). 
   - If 0 files are provided, print `STATUS: EMPTY`.
   - If 1 or more files are provided, and **all** filenames end with the extension `.dat`, print `STATUS: OK, COUNT: <N>` (where `<N>` is the number of files).
   - If any filename does not end with `.dat`, print `STATUS: ERROR`.

4. **Text Processing & Processing Script**:
   Create a bash script at `/home/user/run_tests.sh` that processes the queued jobs. For every `.job` file in `/home/user/spool/`:
   - Read the commit hash (`<newrev>`) from the file.
   - Use `git --git-dir=/home/user/backup_repo.git show <newrev>:restore.log` to extract the `restore.log` file from that specific commit.
   - Using `grep` and `awk`, filter the log to find lines containing the word `RESTORED`. Extract the second word from those lines (which represents the filename).
   - Pipe these extracted filenames into `/home/user/verify_restore`.
   - Save the exact standard output of the C++ program to `/home/user/results/<newrev>.out`.
   - Delete the `.job` file after processing.
   Make sure `/home/user/run_tests.sh` is executable.

5. **Scheduled Task**:
   Create a file at `/home/user/backup_cron.txt` representing a crontab configuration. It should contain exactly one line that schedules `/home/user/run_tests.sh` to run every 5 minutes. Use standard cron syntax.

Complete these steps using bash commands, standard Linux text processing tools, and C++.