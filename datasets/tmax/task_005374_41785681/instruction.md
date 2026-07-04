You are an AI assistant helping with a configuration manager system. We need a Bash script to track changes in binary blobs referenced by configuration files.

Write a Bash script at `/home/user/tracker.sh` that does the following:
1. Searches the directory `/home/user/configs/` for all `.ini` files. 
2. The directory contains some symlinks. You must follow symlinks to find the actual `.ini` files, but be aware that some symlinks form infinite loops. Your script must gracefully avoid getting stuck in these loops and only process the valid, resolvable `.ini` files exactly once per valid physical file.
3. For each valid, unique `.ini` file, extract the binary path defined by the key `BinPath=` (e.g., `BinPath=/path/to/file.bin`).
4. Open the referenced binary file and extract exactly 4 bytes of data starting at offset 8 (0-indexed).
5. Format these 4 bytes as an uppercase hex string with no spaces (e.g., `A1B2C3D4`).
6. Append the extracted hex string to `/home/user/summary.log` in the format `<basename_of_binary>: <HEX_STRING>`. For example, if the binary is `/home/user/binaries/app.bin`, the line should be `app.bin: A1B2C3D4`.
7. Because other tracking processes might be running concurrently, you MUST use `flock` to acquire an exclusive lock on `/home/user/summary.lock` whenever writing to `/home/user/summary.log`.

Make the script executable and run it once so the `/home/user/summary.log` file is generated. Use only standard bash built-ins, coreutils, and standard Linux CLI tools (like `find`, `dd`, `hexdump`, `od`, `grep`, `awk`, etc.). Do not use Python, Perl, or other scripting languages.