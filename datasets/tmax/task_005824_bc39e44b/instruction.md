You are a storage administrator working on a Linux server. You've discovered a directory of large, legacy log files taking up unnecessary space. To reclaim disk space while retaining the data, you need to write a C++ utility that reads these files, converts their character encoding, changes their structural format, and compresses them using a custom algorithm.

Here are the requirements:

1. **Input Location and Format:**
   - The legacy logs are located in `/home/user/legacy_logs/`.
   - The files are named with a `.csv` extension (e.g., `log1.csv`).
   - The files are encoded in **UTF-16LE**.
   - The CSV format contains three columns with a header: `Timestamp,Severity,Message`.

2. **Processing Steps:**
   - Write a C++ program to process all `.csv` files in the input directory.
   - **Encoding Conversion:** Convert the file contents from UTF-16LE to **UTF-8**.
   - **Format Conversion:** Convert the CSV data into a minified JSON array of objects. 
     - Map `Timestamp` to `"t"` (as a numeric literal, not a string).
     - Map `Severity` to `"s"` (string).
     - Map `Message` to `"m"` (string).
     - Example output structure before compression: `[{"t":1670000000,"s":"INFO","m":"System started"}]`
   - **Custom Compression (RLE):** Compress the resulting UTF-8 JSON string using a strict byte-level Run-Length Encoding (RLE). 
     - Every sequence of identical consecutive bytes must be encoded as two bytes: `[Count][Byte]`.
     - `Count` is a single unsigned byte representing the number of repetitions (1 to 255). If a sequence exceeds 255 bytes, start a new `[Count][Byte]` pair.
     - Even single characters must be encoded as `[1][Byte]`.

3. **Output:**
   - Save the compressed binary files to `/home/user/archive/`.
   - The output files should have the same base name as the input, but with a `.json.rle` extension (e.g., `/home/user/archive/log1.json.rle`).
   - To prove your compression works, your C++ program (or a separate C++ program) must also implement the decompression algorithm. Decompress your `.json.rle` files back to UTF-8 JSON strings in memory, compute their SHA-256 hashes, and append the results in the format `<sha256>  <filename>.json` to `/home/user/checksums.txt`. Use standard sha256sum formatting.

You may use standard C++ libraries (`<fstream>`, `<iostream>`, `<vector>`, `<string>`, `<filesystem>`, etc.) and standard Linux commands/packages. If you need to compute SHA-256, you can use system commands via `popen` or install a library like `libssl-dev`. 

Compile and run your code to produce the files in `/home/user/archive/` and the `/home/user/checksums.txt` file.