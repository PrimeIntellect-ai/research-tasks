You are a backup administrator tasked with setting up an automated, highly-compressed archive pipeline for legacy system data. 

There are three main parts to this task:

1. **Fix and Build the Archiver**
We are using a proprietary, highly efficient compression tool called `fast-archiver`. The source code for this tool is vendored at `/app/fast-archiver-1.0/`.
Unfortunately, the previous maintainer made a mistake in the build configuration, and the tool currently fails to build or does not compress data optimally.
Your task is to identify the issue in the `/app/fast-archiver-1.0/Makefile`, fix it, compile the tool, and copy the resulting `fast-archiver` binary to `/home/user/bin/fast-archiver`. Make sure `/home/user/bin` is in your PATH.

2. **Develop the Backup Daemon**
Write a Bash script located at `/home/user/backup_daemon.sh`. This script must:
- Continuously watch the directory `/home/user/spool/` for the appearance of a configuration file named `backup.conf`.
- Once `backup.conf` appears, parse it. The config file will contain key-value pairs (e.g., `TARGET_DIR=/home/user/data`, `EXCLUDE_EXT=.log`).
- Read the `TARGET_DIR` and prepare the data for backup. 
- *Crucial Encoding Step:* Many text files (`.txt`) in the target directories are encoded in legacy `ISO-8859-1`. Your script must find all `.txt` files in the target directory, convert their character encoding to `UTF-8`, and replace the original files.
- After conversion, use the compiled `/home/user/bin/fast-archiver` to compress the target directory. The `fast-archiver` takes two arguments: the input directory and the output file. Compress the `TARGET_DIR` into an archive named `/home/user/final_backup.fsa`.

3. **Execution**
Run your daemon in the background. Then, to trigger it, create a sample configuration file at `/home/user/spool/backup.conf` containing:
```
TARGET_DIR=/home/user/legacy_data
EXCLUDE_EXT=.tmp
```
(Assume `/home/user/legacy_data` already contains the files you need to process). 
Wait for your daemon to generate `/home/user/final_backup.fsa`.

**Verification Constraints:**
To pass this task, the final archive `/home/user/final_backup.fsa` must be correctly formatted, contain UTF-8 encoded text files, and meet strict compression requirements. The archive file size must be less than 4,500,000 bytes.