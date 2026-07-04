You are a backup administrator responsible for implementing a resilient file archiving tool in C. 

We have a server that contains complex directory structures, sometimes with user-created symlinks that inadvertently create infinite loops (e.g., directory A links to B, and B links back to A). Previous shell scripts have crashed or run out of disk space by blindly following these loops.

Your task is to create a robust C program that walks a directory tree, computes MD5 checksums for all regular files, and generates a clean manifest file, gracefully handling symlink loops by tracking visited inodes.

Here are your instructions:
1. We have left an image file at `/app/policy.png`. It contains the backup configuration policy (a scanned document). Use OCR (e.g., `tesseract`) to read the configuration. It will specify a `Target Directory` and an `Output Manifest` path.
2. The `Target Directory` contains several files and directories, including a nasty symlink loop.
3. Write a C program at `/home/user/generate_manifest.c` that takes the `Target Directory` and `Output Manifest` as command-line arguments.
4. The C program must traverse the target directory recursively. It MUST follow symlinks, but it must keep track of the `dev` and `ino` (device and inode numbers) of directories it has visited to prevent infinite loops. If a directory has already been visited in the current path chain (or globally), skip it.
5. For every regular file encountered, calculate its MD5 checksum. (You may use OpenSSL's `libcrypto`, e.g., `#include <openssl/md5.h>`, make sure to link with `-lcrypto`).
6. The program should write to the `Output Manifest` file. Each line should be formatted exactly as:
   `[MD5_HEX] [FILE_SIZE_BYTES] [RELATIVE_PATH]`
   Example: `d41d8cd98f00b204e9800998ecf8427e 1024 data/docs/report.txt`
7. Compile and run your C program to produce the manifest specified in the policy. 

Your solution will be evaluated by an automated metric. The metric computes the F1 score of the discovered unique files in your manifest against the ground-truth list of unique files. Your program must finish execution within 5 seconds (which it will easily do if you properly avoid the infinite loop) and your F1 score must be >= 0.95.