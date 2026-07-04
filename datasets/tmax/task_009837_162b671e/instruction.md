I need help organizing my project's deployed assets into an archive directory without duplicating data. I have a multi-line deployment log that specifies which files were deployed, their deployed names, and any optional aliases.

Here is the setup:
- Source files are located in `/home/user/project/src/`.
- The deployment log is located at `/home/user/project/deploy.log`.
- The archive directory should be `/home/user/archive/` (please create it if it doesn't exist).

The log file has multi-line entries separated by blank lines. Each entry looks like this:
```
[DEPLOY] <date>
Source: <relative path to source file>
Target: <deployed file name>
Alias: <optional alias name>
```

Your task is to write and run a Python script to process this log and do the following:
1. Parse the multi-line records in `/home/user/project/deploy.log`.
2. For each record, create a **hard link** in `/home/user/archive/` named as the `Target`, pointing to the original `Source` file in `/home/user/project/`.
3. If an `Alias` is present in the record, create a **symbolic link** in `/home/user/archive/` named as the `Alias`, which points exactly to the `Target` name (a relative symlink within the archive directory).
4. After creating all links, generate a JSON manifest file at `/home/user/archive/manifest.json`. This file must be a JSON dictionary mapping every file name (including both hard links and symlinks) present in `/home/user/archive/` to the SHA256 checksum of its file *content*. Do not include the `manifest.json` file itself in the manifest.

Ensure you use Python for the logic and only operate within `/home/user/`.