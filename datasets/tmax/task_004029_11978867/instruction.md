You are assisting a researcher who is organizing a large dataset of sensor records. The dataset consists of custom compressed Write-Ahead Logs (WAL). Unfortunately, some of the dataset has been corrupted with malicious/invalid entries.

The researcher left a voice note for you at `/app/research_note.wav` explaining the exact criterion for identifying a malicious WAL file. 

Your task is to write a Go program at `/home/user/wal_filter.go` that acts as a classifier and filter for these files.

**Requirements for `/home/user/wal_filter.go`:**
1. **CLI Arguments:** The program must accept three flags:
   - `-in`: The path to the input directory containing the files.
   - `-out`: The path to the output directory where valid files should be copied.
   - `-log`: The path to a shared log file.
2. **Concurrency & File Locking:** The program must process the files in the input directory concurrently (using goroutines). Whenever a file is classified, the program must append a line to the `-log` file. Because multiple goroutines will write to this log file, you must use proper synchronization (e.g., `sync.Mutex` or file locking) to prevent garbled log entries.
3. **Decompression:** All files in the input directory end with `.wal.rle`. They are compressed using a custom Run-Length Encoding (RLE). The format is a sequence of 2-byte pairs: `[1 byte count (unsigned)][1 byte character]`. For example, `0x03 0x41` decodes to `AAA`.
4. **Parsing:** Once decompressed, the file is a text-based Write-Ahead Log. Each line has the format: `TXN:<transaction_id> DATA:<payload>`. (Example: `TXN:1042 DATA:sensor_temp=45`)
5. **Filtering:** You must determine if the file is valid ("clean") or malicious ("evil") based on the secret rule dictated in `/app/research_note.wav`.
   - If **clean**: Copy the original `.wal.rle` file (still compressed) to the `-out` directory, and append `<filename>: CLEAN\n` to the `-log` file.
   - If **evil**: Do not copy the file, and append `<filename>: EVIL\n` to the `-log` file.

**Example Invocation:**
```bash
go run /home/user/wal_filter.go -in /app/dataset/raw -out /app/dataset/clean -log /home/user/summary.log
```

We will test your program against two hidden corpora. Ensure your code compiles and correctly handles concurrency, parsing, and the secret business logic.