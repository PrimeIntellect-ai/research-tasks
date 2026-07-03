I have a configuration backup archive located at `/home/user/config_backup.tar`. I suspect it might have been tampered with and contains "tar slip" payloads (paths that attempt to write outside the extraction directory, such as absolute paths or paths containing directory traversal sequences like `../`).

Please perform the following operations safely:
1. Examine the archive and extract ONLY the safe files into the directory `/home/user/safe_configs/`. A file is considered safe if its path is relative and does not contain any traversal components (`../` or `..`) that would cause it to be extracted outside the target directory. Do NOT extract any malicious files.
2. Search the extracted safe files in `/home/user/safe_configs/` (and its subdirectories) to find the file with the newest modification time (mtime) based on its file metadata.
3. Create a report at `/home/user/report.txt` containing the base filename and the exact contents of this newest safe file, formatted exactly as follows:

```
Filename: [Base filename]
Content: [File content]
```

Ensure that no malicious files are extracted anywhere on the file system.