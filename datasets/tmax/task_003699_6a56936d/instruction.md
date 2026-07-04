You are an AI assistant helping a technical writer build an automated, real-time documentation archiving and publishing system. 

The writer keeps their raw markdown drafts in `/home/user/docs/src`. They need a Python-based background daemon that continuously watches this directory for changes, maintains a space-efficient "published" mirror using hard links, manages a symbolic link for the live site, and creates incremental backups.

Your task is to write and execute a Python script named `/home/user/doc_daemon.py` that fulfills the following requirements:

1. **File Watching**: Use the Python `watchdog` library to monitor `/home/user/docs/src` for any file creation, modification, or deletion events.
2. **Hard Link Management**: Whenever a file event occurs, instantly sync the `/home/user/docs/published` directory to match the `src` directory. 
   - You MUST use **hard links** to place files in the `published` directory (do not duplicate file contents).
   - If a file is deleted in `src`, its corresponding hard link in `published` must also be deleted.
   - Subdirectories should be created normally as directories, but the files within them must be hard linked.
3. **Symbolic Link**: Ensure there is a symbolic link at `/home/user/docs/live` that points directly to the `/home/user/docs/published` directory. The Python script should create or verify this symlink on startup.
4. **Incremental Backups**: On every single file event detected by `watchdog`, trigger an incremental `tar` backup of the `/home/user/docs/src` directory.
   - Save the backups in `/home/user/docs/backups/`.
   - Use `tar`'s built-in GNU incremental backup feature (`--listed-incremental=/home/user/docs/backups/snapshot.snar`).
   - Name the backup files sequentially starting from 0: `backup_0.tar`, `backup_1.tar`, `backup_2.tar`, etc.
5. **Stream Redirection & Piping**: For every event, the script must `print()` exactly one line to standard output in this exact format: `EVENT: <event_type> | PATH: <filepath>` (e.g., `EVENT: modified | PATH: /home/user/docs/src/draft.md`).

**Execution Instructions:**
1. Write the `/home/user/doc_daemon.py` script.
2. Ensure the target directories (`published`, `backups`) exist.
3. Start your script in the background and redirect its standard output to `/home/user/docs/daemon.log`.
4. Once the daemon is running, execute the pre-existing bash script `/home/user/simulate_writer.sh`. This script will simulate the technical writer working on their files by creating, modifying, and deleting files over the span of a few seconds.
5. Wait for the simulation script to finish entirely.
6. Gracefully kill your background Python daemon.

Verify your work by checking that `/home/user/docs/published` perfectly mirrors the final state of `src` (using hard links), that `daemon.log` is populated, and that multiple incremental `.tar` archives exist in `/home/user/docs/backups/`.