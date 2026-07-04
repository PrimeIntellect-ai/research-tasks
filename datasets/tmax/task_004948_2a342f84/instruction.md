I need your help automating our backup archiving process. We have a legacy system that processes Write-Ahead Log (WAL) files and archives them using a custom, proprietary compression and integrity-checking algorithm. 

The binary that does this is located at `/app/wal_packer`. Unfortunately, the source code was lost years ago, and the binary is stripped. We need to port this tool to Python so we can integrate it into our modern backup pipelines. 

Your task is to write a Python 3 script at `/home/user/wal_packer.py` that behaves EXACTLY like `/app/wal_packer`. 

Here is what we know about the expected behavior:
1. The script should be invoked as: `python3 /home/user/wal_packer.py <input_file> <output_file>`
2. It reads the input file (which contains arbitrary binary data, simulating a WAL file).
3. It performs a specific custom compression/packing algorithm on the data.
4. It writes the packed data to `<output_file>`. To prevent corrupted backups during server crashes, the write operation must be ATOMIC (e.g., writing to a temporary file first, then moving it to the final destination).

To successfully complete this task, you will need to:
- Use tools like `objdump`, `strace`, or `gdb` to reverse-engineer the logic inside `/app/wal_packer`. 
- Find the sample `.wal` files scattered in `/home/user/backup_data/` (you can find them by searching for files modified in the last 24 hours with a size greater than 1KB) to use as test inputs.
- Implement the exact packing logic in Python.

Our CI pipeline will verify your script by fuzzing it with thousands of random files and comparing its output bit-for-bit against the original `/app/wal_packer`. Ensure your Python script accurately handles edge cases and large files identically to the binary.