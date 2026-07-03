You are acting as a backup administrator responsible for securely archiving application logs. The raw logs contain sensitive user passwords that must be redacted before archiving.

Your task is to create a complete redaction and archiving pipeline. 

First, write a C program located at `/home/user/redact.c` that does the following:
1. Reads text line-by-line from standard input (`stdin`).
2. Scans each line for the exact string `PASSWORD=`. 
3. If found, replaces the value immediately following `PASSWORD=` (up to the next whitespace character or newline) with `[REDACTED]`. For example, `USER=admin PASSWORD=supersecret IP=127.0.0.1` should become `USER=admin PASSWORD=[REDACTED] IP=127.0.0.1`.
4. Writes the processed (or unmodified) line to standard output (`stdout`).
5. Compile this program to an executable named `/home/user/redact`.

Second, write and execute a bash script at `/home/user/archive.sh` that performs the following steps:
1. Creates a directory `/home/user/clean_logs`.
2. Finds all `.log` files in the directory `/home/user/raw_logs`.
3. Uses stream redirection/piping to pass the contents of each `.log` file through your compiled `/home/user/redact` program, saving the redacted output to `/home/user/clean_logs/` keeping the same filename.
4. Generates a SHA-256 checksum manifest of all the files inside `/home/user/clean_logs/`. Save this manifest to `/home/user/clean_logs/manifest.sha256` using the standard `sha256sum` format (run from inside the `clean_logs` directory so the paths in the manifest are just the filenames).
5. Creates a compressed tarball archive named `/home/user/backup.tar.gz` that contains the `clean_logs` directory and its contents.

You must ensure that the final `/home/user/backup.tar.gz` is created successfully and contains no unredacted passwords.