I am a researcher organizing 3D printing datasets. I received a custom dataset backup archive named `dataset.bak` located in `/home/user/`. However, I suspect this archive might have been tampered with and contains "Zip Slip" vulnerabilities—malicious file paths designed to overwrite system files outside the intended extraction directory.

I need you to write a Rust program that safely extracts this archive and performs some data analysis on the extracted GCode files.

Here is the specification for the custom `.bak` binary format:
1. **Magic Header**: The file starts with exactly 8 bytes: `DATASET\0`.
2. **File Entries**: Immediately following the magic header is a sequence of file entries until EOF. Each entry consists of:
   - `path_length` (unsigned 16-bit integer, little-endian): The length of the file path in bytes.
   - `path` (UTF-8 string): The file path (length is `path_length`).
   - `file_size` (unsigned 32-bit integer, little-endian): The size of the file content in bytes.
   - `content`: The raw bytes of the file (length is `file_size`).

Your tasks:
1. **Write a Rust program** to parse `/home/user/dataset.bak`.
2. **Zip Slip Prevention**: Iterate through the file entries. If a file path is absolute (starts with `/`) or attempts to traverse up a directory (contains `../`), **do not extract it**. Instead, append the exact malicious path string to a log file at `/home/user/malicious.log` (one path per line).
3. **Safe Extraction**: For all safe paths, extract the files into `/home/user/extracted/` (create this directory if it doesn't exist, and create any necessary subdirectories).
4. **Data Analysis**: After extraction, parse all `.gcode` files in the safe extracted files. For every line that starts with `G1 ` (a linear move command), check if it contains an extrusion command `E` followed by a number (e.g., `G1 X10 Y20 E2.5`). Sum up all the `E` values across all safe GCode files.
5. **Output**: Write the total extrusion sum as a floating-point number (e.g., `4.5`) to `/home/user/extrusion_total.txt`.

Please write and execute the Rust code to accomplish this. Do not worry about malicious files exploiting symlinks for this task, just strictly filter out paths starting with `/` or containing `../`.