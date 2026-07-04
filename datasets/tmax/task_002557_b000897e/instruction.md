You are a build engineer managing firmware artifacts. Our legacy pipeline used a slow Python script (`/home/user/calc_hash.py`) to parse an artifact size expression, read that exact number of bytes from a binary, and compute a custom rolling checksum. 

A junior engineer attempted to rewrite this tool in C (`/home/user/calc_hash.c`) for performance, but the C version is failing. It suffers from memory safety issues (segfaults), undefined behavior in the bitwise operations, and incorrectly parses the mathematical expression compared to the Python reference.

Your task is to:
1. Analyze the reference Python script at `/home/user/calc_hash.py`.
2. Fix the bugs, memory safety issues, and undefined behavior in `/home/user/calc_hash.c` so that it faithfully matches the behavior and output of the Python script. The C program must safely parse a size expression of the form `A*B+C` (where A, B, and C are positive integers).
3. Compile the fixed C code into an executable at `/home/user/calc_hash` using `gcc -O2 -Wall -Werror /home/user/calc_hash.c -o /home/user/calc_hash`.
4. Run your compiled C executable on the artifact `/home/user/firmware.bin` using the size expression `"512*7+13"`.
5. Save the standard output of this run to `/home/user/hash_output.txt`.

The format of `/home/user/hash_output.txt` must be exactly the numeric checksum as a base-10 integer followed by a newline (the same format output by the Python script). Ensure your C code handles the file operations cleanly and does not leak memory.