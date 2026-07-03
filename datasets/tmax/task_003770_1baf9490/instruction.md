You are tasked with helping a configuration management system track recent changes.

You need to write a C++ program at `/home/user/tracker.cpp` that performs the following operations:

1. **Parse an Audit Log:** Read the multi-line log file at `/home/user/audit.log`. The log consists of records in the following format:
   ```
   [RECORD]
   ID: <number>
   File: <filename>
   Status: <CHANGED | UNCHANGED>
   [END]
   ```
   You need to extract the `File` names for all records where the `Status` is `CHANGED`.

2. **Recursive Directory Traversal:** For each changed file, search for it recursively within the `/home/user/config_repo/` directory. 

3. **Character Encoding Conversion:** The configuration files in the repository are encoded in UTF-16LE. When your C++ program reads a located file, it must decode the contents from UTF-16LE into standard UTF-8. 

4. **Output Generation:** Your C++ program must generate a summary log at `/home/user/summary.txt`. 
   For each changed file found, write a block to the summary file in exactly this format:
   ```
   --- <filename> ---
   <UTF-8 decoded contents of the file>
   ```
   Order the files alphabetically by their filename in the output.

**Requirements & Constraints:**
- Use C++17 or later. Compile your program to `/home/user/tracker` and execute it.
- Do not hardcode the file paths of the nested configurations; your code must perform the recursive search.
- The output file `/home/user/summary.txt` must strictly contain only the blocks for the `CHANGED` files.
- Standard libraries only. You may use shell commands within `system()` or standard C++ features for the encoding conversion.