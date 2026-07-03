You are an AI assistant helping a researcher safely process and organize a batch of 3D printer and sensor datasets. 

The researcher has received a custom-packed dataset archive located at `/home/user/dataset.archive`. 
The archive format is a custom text-based serialization. Each file in the archive is represented as follows:

```
[FILE_START]
<file_path>
[CONTENT_START]
<file_contents>
[FILE_END]
```

Your task is to write and execute a Bash script (`/home/user/process_dataset.sh`) to perform the following:

1. **Safe Extraction (Custom Decompression & Path Security)**
   Extract the contents of `/home/user/dataset.archive` into the `/home/user/extracted/` directory. 
   **Security Warning:** This archive is from an untrusted source and may contain a "zip slip" style vulnerability. Your script MUST NOT extract any file whose path attempts to escape the `/home/user/extracted/` directory (e.g., paths starting with `/` or containing `..`). Skip these malicious files entirely and do not write them anywhere.
   Make sure to create any necessary parent directories inside `/home/user/extracted/` for the valid files.

2. **Atomic Writes**
   When writing the valid extracted files, use atomic writes. Write the extracted content to a temporary file (e.g., `<filename>.tmp`) first, and only when the file content is fully written, move (`mv`) it to its final destination path inside `/home/user/extracted/`.

3. **Domain Parsing & Symbolic Link Organization**
   After extraction, analyze all the `.gcode` files present in `/home/user/extracted/`. 
   Read the contents of each `.gcode` file:
   - If the file contains the GCode command `G28` (Auto Home), categorize it as "calibration".
   - If the file does NOT contain `G28`, categorize it as "production".
   
   Create symbolic links to these extracted files in the `/home/user/organized/` directory structure. 
   Create two subdirectories: `/home/user/organized/calibration/` and `/home/user/organized/production/`.
   Inside these directories, create symbolic links pointing to the absolute paths of the corresponding categorized `.gcode` files. Use the exact base name of the original file for the symlink. (If multiple files have the same base name, you may overwrite the link, but for this dataset, base names are unique).

4. **Verification Log**
   Once finished, create a log file at `/home/user/symlink_report.log`.
   The log file must contain the absolute paths of all created symbolic links and their targets, in the following format (sorted alphabetically by link path):
   `<symlink_path> -> <target_path>`

Ensure your script is executable and execute it to complete the task.