I'm organizing my project files using an automated pipeline, but I've realized my archive extraction sanitization tool has a vulnerability. My pipeline uses three services: a lightweight FTP server (vsftpd) for uploads, an inotify-wait script that monitors the upload directory, and a custom C program `filter_paths` that checks the contents of uploaded archives before they are moved to a safe storage directory. 

Currently, the `filter_paths` C program does not properly detect path traversal attempts (like `../` or absolute paths `/etc/passwd`). I need you to rewrite `/home/user/app/filter_paths.c` so that it correctly sanitizes incoming file paths.

Your C program must compile to `/home/user/app/filter_paths` and accept a single argument: the path to a text file containing a list of file paths (one per line) extracted from an archive. 
- It must output `SAFE` to stdout if all paths in the file are safe (no absolute paths starting with `/`, and no directory traversal components like `../` or `..` as a path segment).
- It must output `MALICIOUS` to stdout if ANY path in the file contains absolute paths or directory traversal components.
- Ignore empty lines.

After fixing the C code, ensure you compile it using `gcc -o /home/user/app/filter_paths /home/user/app/filter_paths.c`. Finally, restart the inotify-watcher service so the pipeline uses your new binary.

The pipeline services are:
- `vsftpd` running on port 21
- `redis-server` running on port 6379 (used for logging safe/malicious counts)
- `watcher.sh` running as a background process monitoring `/home/user/ftp/uploads/`

Your fix will be tested against a hidden corpus of clean and malicious path lists.