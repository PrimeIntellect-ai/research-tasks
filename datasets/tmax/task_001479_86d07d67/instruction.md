You are acting as a storage administrator managing disk space and backup restorations. Recently, your automated backup extraction system was compromised via a "Zip Slip" style vulnerability, where maliciously crafted backup manifests extracted files outside the intended directories, overwriting system files.

Your task is to write a secure C++ program that processes backup manifests, safely writes the files to disk using atomic operations, enforces disk space limits, and generates a checksum manifest of the extracted files.

Here are your requirements:

1. **Environment Setup:** 
   You have a configuration file at `/home/user/config.json` and a backup manifest at `/home/user/manifest.json`.
   Create a directory `/home/user/extracted` to store the output files.

2. **Program Specifications:**
   Write a C++ program at `/home/user/extractor.cpp` that takes two command-line arguments: the path to the config JSON and the path to the manifest JSON.
   
   **Configuration Format (`config.json`):**
   ```json
   {
     "allowed_base_dir": "/home/user/extracted",
     "max_total_bytes": 500
   }
   ```

   **Manifest Format (`manifest.json`):**
   A JSON array of file objects to restore:
   ```json
   [
     {
       "path": "file1.txt",
       "content": "This is a test file."
     },
     ...
   ]
   ```

3. **Security and Transformation Rules:**
   - **Path Sanitization (Zip Slip Prevention):** The program must iterate over the manifest. If a `path` contains the substring `..` or starts with `/` (an absolute path), it must be **completely skipped**. 
   - **File Writing (Atomic):** For allowed files, the destination path is `<allowed_base_dir>/<path>`. You must ensure atomic writes. Specifically, open and write the content to `<allowed_base_dir>/<path>.tmp`. Only after the file is fully written and closed should you rename it to `<allowed_base_dir>/<path>`. Create any necessary subdirectories.
   - **Quota Management:** Keep a running total of the bytes written. If writing a file would cause the total extracted bytes to exceed `max_total_bytes` from the config, skip that file and all subsequent files.

4. **Checksum Manifest:**
   After processing the manifest, the C++ program must generate a CSV file at `/home/user/extraction_report.csv`.
   The CSV must have the header `filepath,sha256` and contain a row for every successfully written file (using its relative path from the manifest). Use standard SHA256 hashing.

5. **Execution:**
   Compile your program using `g++` (you may link against `-lcrypto` for OpenSSL hashing and use standard JSON parsing headers or system tools if available. A standalone JSON parser header like `nlohmann/json.hpp` can be downloaded into your directory via `wget https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp` if needed).
   Execute the compiled program with the provided `/home/user/config.json` and `/home/user/manifest.json`.

Write the code, compile it, and run it successfully to produce the final extracted files and the `extraction_report.csv`.