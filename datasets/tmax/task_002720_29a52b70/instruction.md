You are helping a developer organize their project backup archives. 

In `/home/user/archives/`, there are several zip files representing different project backups. However, some of these backups failed during transfer and are corrupted. 
There is a log file at `/home/user/backup_history.log` that maps project versions to these archive files using a multi-line format.

The log file has records separated by a blank line. Each record looks exactly like this:
```
Record Start
Version: <version_string>
Archive: <absolute_path_to_zip>
Status: complete
```

Your task is to write and execute a C++ program named `/home/user/organizer.cpp` that performs the following actions:
1. Parses the multi-line log file `/home/user/backup_history.log`.
2. For each record, verifies the integrity of the specified zip archive (you may use `std::system` to invoke standard CLI tools like `unzip` for testing).
3. If the zip file is valid and completely intact, creates a symbolic link in the directory `/home/user/valid_backups/` named `<version_string>_link.zip` that points to the original archive file.
4. If the zip file is corrupted or invalid, ignores it and creates no link.

Requirements:
- Ensure the `/home/user/valid_backups/` directory exists before creating links (your program or shell commands can create it).
- Only use standard C++ libraries and basic shell tools (bash-only environment).
- You must write the logic in C++, compile it to `/home/user/organizer`, and run it to produce the final state.