You are tasked with organizing and securing a massive influx of legacy project archives. The archives are in a custom proprietary format (`.pdat`). 

We have a legacy compiled tool, `/app/validator`, which correctly validates `.pdat` archives and checks them for corruption or malicious directory traversal attempts. However, this legacy tool is incredibly slow, and the original source code is lost.

Your objective is to:
1. Reverse-engineer the validation logic of the stripped binary `/app/validator`. You can analyze it statically or treat it as a black-box oracle by feeding it test files. It takes a single file path as an argument and returns exit code `0` for valid/safe files, and `1` for invalid/corrupt/malicious files.
2. Write a highly efficient C program at `/home/user/pdat_filter.c` that replicates the exact validation logic of the legacy tool. Compile it to `/home/user/pdat_filter`. Your program must accept a file path as its first CLI argument `argv[1]` and exit with `0` if the archive is valid/safe, and `1` if it is not.
3. The legacy tool is known to parse file structures, check archive integrity (offsets and sizes), and inspect embedded filenames which are known to be encoded in UTF-16LE. You will need to handle this character encoding to properly detect path traversal payloads (e.g., `../`).
4. Write a bash script `/home/user/watch.sh` that uses `inotifywait` to watch the directory `/home/user/incoming/` for new files (`close_write` events). When a file is written:
   - Run your `/home/user/pdat_filter` on the new file.
   - If it exits 0, move the file to `/home/user/accepted/`.
   - If it exits 1, move the file to `/home/user/rejected/`.
   - Append the result in the format `[TIMESTAMP] FILE_NAME: STATUS` (where STATUS is ACCEPTED or REJECTED) to `/home/user/process.log` using standard stream redirection.

To help you, there is a sample valid archive at `/app/sample.pdat`.
Your C program will be tested against a massive hidden corpus of clean and malicious `.pdat` files. It must exactly match the legacy tool's exit codes.