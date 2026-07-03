We are building a configuration management tracker that creates signatures of configuration files. However, our configuration directory often contains messy symbolic links, including broken links and infinite symlink loops, which have crashed our backup scripts in the past.

Your task is to write a C program that reads a list of files from a configuration file, resolves their paths safely, extracts their binary headers, and outputs the data in a specific format.

**Requirements:**

1. Create a C program at `/home/user/tracker.c`.
2. The program must take exactly one command-line argument: the path to a configuration file. For this task, it will read `/home/user/backup.conf`.
3. The configuration file contains a list of absolute file paths, one per line.
4. For each path in the file:
   - Safely resolve the symbolic links to find the ultimate target. 
   - If the path is a broken symlink, or forms an infinite symlink loop (cannot be resolved), you must skip it and print `SKIP: <original_path_from_conf>` followed by a newline to **standard error** (`stderr`).
   - If the path resolves to a valid file, retrieve the inode number of the *resolved* ultimate file (not the symlink).
   - Open the resolved file and read exactly the first 8 bytes (the header). If the file has fewer than 8 bytes, pad the remaining bytes with null bytes (`0x00`).
   - Convert these 8 bytes into a lowercase hexadecimal string (16 characters long).
   - Print the result to **standard output** (`stdout`) in this exact format: `<original_path_from_conf>|<resolved_inode>|<hex_encoded_8_bytes>\n`
5. Compile your program to `/home/user/tracker`.
6. Run your program with `/home/user/backup.conf` as the argument. Redirect standard output to `/home/user/tracker_out.txt` and standard error to `/home/user/tracker_err.txt`.

**Example:**
If `/home/user/backup.conf` contains `/home/user/config_tree/link_ok`, and it points to `file1.bin` (inode 12345, starting with "MAGIC123"), `tracker_out.txt` should contain:
`/home/user/config_tree/link_ok|12345|4d41474943313233`