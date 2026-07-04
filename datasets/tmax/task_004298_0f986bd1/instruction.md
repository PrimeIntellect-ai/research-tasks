You are a storage administrator managing incoming automated data dumps. Recently, a vulnerability was discovered where extracted nested archives contained directory traversal paths (a "zip slip" attack), attempting to overwrite system files outside the target directory.

Your task is to build an automated pipeline to securely process multi-part incoming archives and log any malicious paths without extracting the vulnerable contents. 

You must complete the following steps:

1. Create the necessary directories:
   - `/home/user/incoming` (where incoming archive parts arrive)
   - `/home/user/workspace` (where your scripts and code will reside)
   - `/home/user/logs` (where results will be logged)

2. Write a C program named `/home/user/workspace/safepipe.c` that acts as a path validator:
   - It must read lines (file paths) from standard input continuously.
   - If a path contains the exact string `../` OR starts with a forward slash `/`, it is considered malicious. The program must append this malicious path to `/home/user/logs/alerts.log` (one path per line) and MUST NOT output it to standard output.
   - If a path is safe, it must be printed to standard output.
   - Compile this program to `/home/user/workspace/safepipe`.

3. Write a bash script `/home/user/workspace/monitor.sh` that watches for incoming multi-part archives:
   - Use `inotifywait` to monitor the `/home/user/incoming` directory for the `close_write` or `moved_to` event of a file named `dump.tar.ab` (which signifies the final part of a split archive has arrived).
   - Once `dump.tar.ab` is detected, the script should concatenate `dump.tar.aa` and `dump.tar.ab` from the incoming directory and pipe standard output to extract the tarball into `/home/user/workspace/`.
   - The extracted tarball will contain a nested archive named `payload.tar.gz`.
   - The script must then list the contents of `payload.tar.gz` (without extracting it) and pipe standard output into your compiled `safepipe` C program.
   - Redirect the standard output of `safepipe` to append to `/home/user/logs/safe.log`.

4. Test your pipeline:
   - Start your `monitor.sh` script in the background.
   - We have staged a multi-part archive in `/tmp/staging/`. Copy `/tmp/staging/dump.tar.aa` to `/home/user/incoming/` first.
   - Then copy `/tmp/staging/dump.tar.ab` to `/home/user/incoming/` to trigger your watcher.

If your watcher and C program are implemented correctly, the malicious paths will be caught in `alerts.log` and the safe paths in `safe.log`.