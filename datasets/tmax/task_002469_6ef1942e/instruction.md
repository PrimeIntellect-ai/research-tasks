I need help organizing and optimizing a messy legacy project directory located at `/app/project_files/`. The previous developer left behind a mix of corrupted archives, oddly-encoded logs, and a scanned note with critical configuration parameters. 

Here is what you need to do:

1. **Extract Configuration from Image:**
   There is a scanned note at `/app/project_files/settings_scan.png`. Use `tesseract` to read the text from this image. It contains a specific character encoding (e.g., `ENCODING=...`) and a numeric duration threshold (e.g., `THRESHOLD=...`). You will need these for the next steps.

2. **Archive Integrity and Organization:**
   The `/app/project_files/archives/` directory contains several `.tar.gz` files. Some are corrupted. Verify the integrity of each archive. Extract the contents of the valid archives into `/app/project_files/extracted/` and move the corrupted archive files themselves into `/app/project_files/corrupted/`. 

3. **Log Parsing and Encoding Conversion:**
   In `/app/project_files/logs/`, there is a multi-line log file named `system.log`. It is encoded in the character encoding specified in the scanned image. 
   - Convert this file to UTF-8.
   - The log contains multi-line entries separated by `---`. Each entry has a `Duration: <number>ms` field. 
   - Use `awk`, `sed`, or a script to filter this log, keeping ONLY the multi-line blocks where the `Duration` is GREATER THAN OR EQUAL TO the threshold found in the scanned image. 
   - Save the filtered, UTF-8 encoded text to `/app/project_files/logs/filtered_system.log`.

4. **C-based Binary Packing (Optimization):**
   The filtered log file is still too large. Write a C program at `/app/project_files/packer.c` that reads `/app/project_files/logs/filtered_system.log` and packs it into a highly compressed custom binary file at `/app/project_files/optimized.bin`. 
   - You must parse the text and implement a simple compression scheme in C (e.g., dictionary encoding for common repeated log keywords, run-length encoding, or stripping redundant whitespace/separators while maintaining the data).
   - Compile your C program and run it to generate `optimized.bin`.
   
To succeed, your C program must compress the filtered log efficiently. The automated test will check the size of `/app/project_files/optimized.bin`. It must be significantly smaller than the raw filtered text file.