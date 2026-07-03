You are helping a developer organize and analyze some poorly structured project files. An old, buggy log rotation script archived our production logs by zipping them, and then a secondary cron job tarred those zips without any clear structure. 

You need to write a Python script at `/home/user/scan_logs.py` that searches through these nested archives to find specific error messages. 

The archives are located in the directory `/home/user/archive_mess/`. 
Inside this directory, there are multiple `.tar` files. 
Inside each `.tar` file, there are one or more `.zip` files. 
Inside each `.zip` file, there are `.txt` log files.

Your script must:
1. Recursively traverse `/home/user/archive_mess/` to find all `.tar` files.
2. Open the `.tar` files and process the `.zip` files inside them *in-memory* (do not extract the archives to disk).
3. Open the `.zip` files *in-memory* and read the `.txt` files.
4. Search every line of the `.txt` files for the exact string: `ERROR_STATE_RACE_CONDITION`
5. Whenever a matching line is found, write it to `/home/user/found_errors.log`.

The format for each line in `/home/user/found_errors.log` must be exactly:
`[outer_tar_filename] -> [inner_zip_filename] -> [txt_filename]: [exact line from the log file including the newline]`

For example:
`group1.tar -> serviceA.zip -> server.txt: 2023-10-01 12:00:00 - ERROR_STATE_RACE_CONDITION detected in thread 4`

Make sure your script executes successfully and generates the `/home/user/found_errors.log` file with the correct contents. Execute your script to complete the task.