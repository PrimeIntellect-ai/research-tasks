I am a researcher trying to organize a messy dataset of observations from different field sensors. The data is currently scattered across various subdirectories in `/home/user/raw_data/`, and unfortunately, the sensors output text in different character encodings. 

I need you to write a Go program at `/home/user/cleaner.go` that normalizes this dataset. 

Here are the exact requirements for the Go program:

1. **Initialization:** Your Go program should be part of a module. You may need to initialize it and fetch necessary dependencies (like `golang.org/x/text` for encoding conversions) in `/home/user/`.
2. **Recursive Traversal:** The program must recursively walk through `/home/user/raw_data/`.
3. **Encoding Conversion:** Find all files ending in `.txt`. The encoding of each file is specified in its filename right before the `.txt` extension (e.g., `sensor1.win1252.txt` is encoded in Windows-1252, `sensor2.utf16le.txt` is UTF-16LE, and `sensor3.utf8.txt` is already UTF-8). You must read the content and convert it to valid UTF-8. 
4. **Path Manipulation:** Save the converted UTF-8 files into `/home/user/clean_data/`. The internal directory structure must exactly mirror the `raw_data` directory. The new filenames should strip the encoding indicator (e.g., `sensor1.win1252.txt` becomes `sensor1.txt`).
5. **Atomic Writes:** To prevent data corruption in case of a crash, you MUST use atomic writes. Write the converted data to a temporary file in a `/home/user/clean_data/.tmp/` directory first, and only after the write is completely successful, rename (move) it to its final destination path.
6. **Summary Log:** After processing all files, the program must write a summary log to `/home/user/summary.txt`. The file should contain exactly two lines:
   - Line 1: The total number of files processed.
   - Line 2: The total number of bytes written across all final UTF-8 files.

Please create, compile, and run this Go program to process the dataset.