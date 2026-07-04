You are an AI assistant helping a data researcher clean up and aggregate a messy dataset. 

The researcher has a directory located at `/home/user/dataset` containing several subdirectories with raw data files ending in `.dat`. Unfortunately, a broken backup script previously ran on this directory and created several recursive symlinks that point back to parent directories, creating infinite symlink loops. 

Your task is to create a reliable aggregation pipeline:

1. Write a shell script at `/home/user/run.sh` that securely finds all real (non-symlink) `.dat` files within `/home/user/dataset` and its subdirectories, completely avoiding the infinite symlink loops. 
2. The shell script should pass these file paths to a Go program that you must write at `/home/user/aggregator.go`.
3. The Go program must process all provided files **concurrently** (using goroutines).
4. For each `.dat` file, the Go program needs to parse the contents. The files are pipe-separated with three columns: `id|measurement|timestamp`.
5. Data Cleaning: 
   - Every `.dat` file has a messy header line starting with `##RAW_DATA` which must be ignored.
   - Some rows contain the exact string `INVALID_ROW`. These rows must be completely skipped.
6. Data Conversion: Valid rows must be converted to JSON objects in the format: `{"id":"<id>","measurement":"<measurement>","timestamp":"<timestamp>"}`.
7. Aggregation: The Go program must append the generated JSON objects to a single output file at `/home/user/master_dataset.jsonl` (one JSON object per line).
8. **Critical requirement:** Because your Go program is processing files concurrently and appending to a single file, you **must** use POSIX file locking (`syscall.Flock` with `syscall.LOCK_EX`) on the output file during every write operation to ensure data is not interleaved or corrupted.

Once you have written both `/home/user/run.sh` and `/home/user/aggregator.go`, execute `/home/user/run.sh` to produce the final `/home/user/master_dataset.jsonl` file. Make sure `/home/user/run.sh` is executable.