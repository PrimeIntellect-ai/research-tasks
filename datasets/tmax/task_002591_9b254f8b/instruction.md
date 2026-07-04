You are tasked with helping a developer organize a chaotic directory of binary project asset files. The assets are located in `/home/user/assets/` and have a `.bin` extension. 

Some of these files are valid project assets, while others are corrupted or irrelevant. We need to extract metadata from the valid ones and compile a central inventory log. Because there are many files, the extraction process must be run concurrently, which means you must handle file locking safely to prevent race conditions when writing to the log.

Here are your instructions:

1. **Write a C program** at `/home/user/extractor.c` that reads exactly 16 bytes from standard input (`stdin`).
2. The 16 bytes represent a binary header with the following little-endian fields:
   - Bytes 0-3: Magic Number (32-bit unsigned integer)
   - Bytes 4-7: Project ID (32-bit unsigned integer)
   - Bytes 8-15: Timestamp (64-bit unsigned integer)
3. The program should check if the Magic Number exactly matches `0xDEADBEEF`.
4. If it matches, the program must open `/home/user/inventory.log` in append mode, acquire an exclusive file lock (using `flock` or `fcntl` to prevent concurrent write corruption), and append a line strictly in this format:
   `ProjectID: <Project ID>, Timestamp: <Timestamp>\n`
   *(Replace the bracketed values with the decimal representations of the extracted numbers).*
5. Release the lock and close the file. If the magic number does not match, the program should exit silently with code 0.
6. **Compile** your C program to an executable named `/home/user/extractor`.
7. **Write and execute a Bash script** at `/home/user/organize.sh` that finds all `.bin` files in `/home/user/assets/` and processes them concurrently using at least 4 parallel background jobs or `xargs -P 4`. The script must pipe or redirect the contents of each `.bin` file into the compiled `extractor` executable.
8. Once all concurrent jobs have finished, your script must sort `/home/user/inventory.log` numerically by ProjectID and save the output to `/home/user/inventory_sorted.log`.

Make sure all files are created in `/home/user/`. You do not have root access, so ensure you write your code to handle standard user permissions.