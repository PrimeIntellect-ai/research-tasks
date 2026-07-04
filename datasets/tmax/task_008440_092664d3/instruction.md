You are tasked with organizing and verifying a set of fragmented binary files for a project. The previous developer left the files in `/home/user/project_data/`, but the directory structure is messy and contains a dangerous symlink loop that crashes standard backup tools.

Your goal is to write a Python script at `/home/user/organize.py` that accomplishes the following:

1. **Safe Traversal & Merging**: 
   Search through `/home/user/project_data/` and all subdirectories for files matching the pattern `part_*.bin` (e.g., `part_1.bin`, `part_2.bin`). You must safely handle or ignore symlinks to avoid falling into infinite loops.
   Merge these files in numerical order (based on the number in the filename) into a single new file located at `/home/user/merged.bin`.
   
2. **File Locking**:
   When writing to `/home/user/merged.bin`, you must acquire an exclusive file lock (e.g., using `fcntl.flock` with `LOCK_EX`) to simulate safe concurrent access, releasing it when done.

3. **Memory-Mapped Verification**:
   There is a reference file located at `/home/user/project_data/reference.bin`. 
   Using memory-mapped I/O (`mmap`), compare the contents of your newly created `/home/user/merged.bin` against `/home/user/project_data/reference.bin`. 
   If the files are exactly identical, write the word `MATCH` to `/home/user/result.txt`. If they differ, write `MISMATCH`.

4. **Streaming Splitting**:
   Take the `/home/user/project_data/reference.bin` file and split it into chunks of exactly 1 MB (1,048,576 bytes). Name the output files `/home/user/split_0.bin`, `/home/user/split_1.bin`, etc. 
   You must use streaming (reading and writing in smaller chunks, e.g., 64KB at a time) rather than loading the entire file into memory to perform this split.

Run your script to produce `/home/user/merged.bin`, `/home/user/result.txt`, and the `/home/user/split_X.bin` files.