You are a storage administrator managing disk space across a fleet of servers. You have been given a set of nested archives containing system logs from multiple servers, and you need to extract specific critical alerts safely.

Your task is to extract these logs concurrently and write a C utility to ensure the output is not corrupted by parallel writes.

1. **Write a C program** at `/home/user/safe_writer.c` and compile it to `/home/user/safe_writer` (using `gcc`).
   - The program must take exactly one command-line argument: the path to an output file.
   - It must read text line-by-line from `stdin`.
   - For every line that contains the exact substring `[DISK_FULL]`, it must append that line to the output file.
   - **Crucial:** Because multiple instances of this program will run concurrently, you MUST use POSIX file locking (`fcntl` with `F_SETLKW` and `struct flock`) to lock the output file exclusively while writing each line, to prevent interleaved/corrupted lines.
   - Ensure the file is created if it doesn't exist, and opened in append mode.

2. **Write a bash script** at `/home/user/extract.sh`.
   - The script must find all `.tar` files in the directory `/home/user/archives/`.
   - Each `.tar` file contains exactly one file: a nested archive named `logs.zip`.
   - Inside `logs.zip` is a text file.
   - For each `.tar` file, your script must extract the `logs.zip` stream to standard output, extract the text contents of the zip to standard output, and pipe the result into your `./safe_writer` program.
   - The target output file for `safe_writer` must be `/home/user/disk_alerts.log`.
   - **Performance requirement:** The extraction and processing for each `.tar` file must be launched concurrently in the background. The script must wait for all background processes to finish before exiting.

Ensure both the C program and the bash script have executable permissions. Once complete, execute your bash script to generate `/home/user/disk_alerts.log`.