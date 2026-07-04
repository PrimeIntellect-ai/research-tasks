You are a storage administrator tasked with managing disk space by implementing a custom incremental backup filter for our application servers. 

We have a legacy, stripped proprietary binary located at `/app/legacy_packer`. This tool compresses text files into a highly efficient custom archive format, but it is notoriously slow and crashes if fed unnecessary data. 

Your goal is to write a Python script, `/home/user/incremental_backup.py`, that prepares only the necessary data for the packer to minimize the final archive size.

Here are your requirements:
1. **Configuration Parsing:** Read `/home/user/backup_config.json`. It contains a key `"target_directories"` (a list of paths) and `"last_run_timestamp"` (an integer Unix timestamp).
2. **Incremental Search:** Search the target directories for all `.log` files that have been modified *strictly after* the `last_run_timestamp`.
3. **Multi-line Log Parsing:** The log files contain multi-line entries. Each entry starts with a timestamp in `[YYYY-MM-DD HH:MM:SS]` format followed by a log level (`[INFO]`, `[DEBUG]`, `[WARNING]`, `[ERROR]`, or `[CRITICAL]`). 
4. **Filtering:** Parse these modified files and extract *only* the log entries (and their accompanying multi-line stack traces or data) that are marked as `[ERROR]` or `[CRITICAL]`. An entry continues until the next timestamp/log level marker.
5. **Staging:** Save the filtered contents into a new directory `/home/user/staging/`, preserving the original file names.
6. **Archiving:** Execute the legacy packer to compress the staging directory. The command syntax is: `/app/legacy_packer -i /home/user/staging -o /home/user/incremental.pak`.

You must execute your script and generate the final `/home/user/incremental.pak` file. To pass, the final archive must be successfully created and its file size must fall below a specific size threshold, proving that your incremental filtering and multi-line parsing were strictly correct.