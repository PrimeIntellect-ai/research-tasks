You are tasked with building a lightweight configuration tracking tool in C++ that generates a file manifest for backups, while safely navigating potentially dangerous directory structures.

In `/home/user`, there is a configuration file named `backup.conf` containing the following key-value pairs:
```
TARGET=/home/user/config_data
OUTPUT=/home/user/manifest.txt
```

The directory `/home/user/config_data` contains various configuration files, subdirectories, and crucially, a symlink that creates an infinite directory loop. 

Your objective is to write a C++ program at `/home/user/tracker.cpp` that does the following:
1. Reads `backup.conf` to determine the `TARGET` directory and the `OUTPUT` file path.
2. Recursively traverses the `TARGET` directory.
3. **Crucial:** Detects and entirely ignores all symlinks to avoid falling into infinite loops.
4. For every regular file found, reads its contents as binary and computes a simple 8-bit checksum (the sum of all bytes in the file modulo 256).
5. Writes a manifest to the `OUTPUT` file. Each line must represent a regular file and be formatted exactly as:
   `<absolute_file_path> <file_size_in_bytes> <8-bit_checksum>`
   (e.g., `/home/user/config_data/app.ini 14 205`)
6. The final `OUTPUT` file must have its lines sorted alphabetically by the file path. You can achieve this by sorting in C++ or using standard shell commands after your program runs.

Compile your C++ program using at least the C++17 standard (`-std=c++17`), run it, and ensure the resulting `/home/user/manifest.txt` is perfectly formatted and sorted.