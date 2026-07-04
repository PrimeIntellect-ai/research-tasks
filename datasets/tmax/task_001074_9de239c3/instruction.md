You are helping a researcher organize a messy dataset of sensor readings. 

In `/home/user/raw_data/`, there is a master archive named `dataset.zip`. This archive contains several nested archives (tar.gz files). 

Your task is to write a Go program at `/home/user/process_dataset.go` that performs the following:

1. **Extraction and Traversal**: 
   - Extract `dataset.zip` to a temporary directory (using standard temporary directory patterns).
   - Recursively traverse the extracted directory to find all `.tar.gz` files.
   - Extract each `.tar.gz` file found into the same directory it resides in.
   - Recursively traverse the newly extracted files to find all `.txt` sensor files.

2. **Concurrent Processing & File Locking**:
   - Launch a goroutine to process each `.txt` file found. Each `.txt` file contains a single integer.
   - Every goroutine must read the integer, then append a line to a shared log file at `/home/user/aggregated_log.tmp` in the format: `[filename]:[value]` (e.g., `sensor_A1.txt:42`).
   - **Constraint**: Because multiple goroutines are writing to the same file, you must use OS-level file locking (e.g., `syscall.Flock` with `syscall.LOCK_EX`) on `/home/user/aggregated_log.tmp` around the write operation to prevent corruption.

3. **Atomic Write**:
   - Once all goroutines have finished writing, the main goroutine should read `/home/user/aggregated_log.tmp`, sort the lines alphabetically, and write them to a new temporary file.
   - Finally, use an atomic rename operation to move the sorted temporary file to the final destination: `/home/user/final_summary.txt`.

Write the program, compile it, and run it so that `/home/user/final_summary.txt` is generated correctly.