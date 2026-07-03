You are acting as a configuration manager tracking changes across a sprawling legacy server environment. Backups of the configuration files are scattered throughout the directory tree at `/home/user/configs/`. 

These backup files end in `.bak`. They have been compressed and encoded using a custom legacy archival tool. 
Your task is to traverse the directory, verify the integrity of these archives, decompress them using a custom C++ program you will write, convert their text encoding, and finally use shell utilities to extract specific tracked changes.

Here is the specification for the `.bak` files:
1. **Custom Compression**: The file is a binary file using a simple Run-Length Encoding (RLE). The file consists of a sequence of 2-byte pairs. The first byte is an unsigned 8-bit integer representing the `count` (number of repetitions). The second byte is the `character` itself.
2. **Checksum**: The very last byte of the `.bak` file is an 8-bit checksum. It is calculated as the sum of the byte values of all *uncompressed* characters, modulo 256. (Note: The 2-byte pairs stop before this final checksum byte).
3. **Encoding**: The uncompressed characters represent text encoded in `ISO-8859-1`.

Your requirements:
1. Navigate through `/home/user/configs/` to find all `.bak` files.
2. Write a C++ program (e.g., `decoder.cpp`) that reads a `.bak` file, verifies its checksum, and decompresses it.
3. If the checksum is invalid, your C++ program should silently skip generating an output file.
4. If the checksum is valid, your C++ program must convert the uncompressed `ISO-8859-1` text to standard `UTF-8` and write it to a new file in the exact same directory, replacing the `.bak` extension with `.cfg`.
5. After all valid configurations have been extracted, use text transformation tools (like `awk` or `sed`) to search through all the newly created `.cfg` files. 
6. Extract any line that starts exactly with `TRACKED_CHANGE=`. 
7. Format your extracted data as `[filename]: [value]` (where `[filename]` is just the base name of the file, e.g., `node1.cfg`, and `[value]` is the part after the `=`).
8. Sort the output alphabetically by filename and save it exactly to `/home/user/tracked_changes.log`.

Example log format:
db_master.cfg: update_v2
web_front.cfg: £40_budget_fix

Ensure your final log file is properly formatted and contains only the valid, correctly decoded entries.