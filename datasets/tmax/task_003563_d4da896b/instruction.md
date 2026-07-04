You are tasked with writing a C program that acts as a simple configuration manager. It will track changes to configuration files in a specific directory by computing checksums, comparing them to a previously saved binary state file, generating a JSON report of the changes, and updating the state file.

Here are the specific requirements:

1. **Target Directory**: The directory to monitor is `/home/user/configs`. It contains various text files ending in `.conf`.
2. **State File**: The previous state is stored in a binary file at `/home/user/state.bin`. 
3. **Checksum Algorithm**: For each file, calculate a simple 8-bit checksum: the sum of all byte values in the file, modulo 256. (e.g., if the file contains "AB", the sum is 65 + 66 = 131. 131 % 256 = 131).
4. **Binary Format**: `/home/user/state.bin` consists of a sequence of 64-byte records. Each record represents a tracked file and is formatted strictly as:
   - Bytes 0-62: The filename (NOT the full path, just the basename, e.g., "app.conf"). Null-terminated and padded with null bytes.
   - Byte 63: The 8-bit unsigned integer checksum of the file.
5. **Operation**:
   - Write a C program in `/home/user/config_tracker.c`.
   - When executed, the program must scan `/home/user/configs` for all files ending in `.conf`.
   - Calculate the current checksum for each `.conf` file.
   - Read `/home/user/state.bin` to get the previous state.
   - Compare the current files and their checksums against the previous state to categorize them into: `added`, `modified`, `deleted`, and `unchanged`.
   - Output a JSON report to `/home/user/config_diff.json`.
   - Overwrite `/home/user/state.bin` with the newly computed current state (using the exact same 64-byte binary format).

6. **JSON Output Format**:
   The file `/home/user/config_diff.json` must exactly match this format (with standard JSON formatting, 2-space indentation, and lists sorted alphabetically by filename):
   ```json
   {
     "added": [
       "file1.conf"
     ],
     "deleted": [
       "file2.conf"
     ],
     "modified": [
       "file3.conf"
     ],
     "unchanged": [
       "file4.conf"
     ]
   }
   ```
   *Note: Ensure the arrays are always present in the JSON even if they are empty (e.g., `[]`).*

Please write, compile, and run your C program to fulfill these requirements. Leave the generated `/home/user/config_diff.json` and the updated `/home/user/state.bin` on the disk for verification.