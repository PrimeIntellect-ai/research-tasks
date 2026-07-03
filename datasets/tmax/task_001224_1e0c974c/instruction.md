You need to help organize and back up a messy project directory by writing a C++ utility that performs an incremental backup based on file checksums. 

Your task is to write and execute a C++17 program at `/home/user/archiver.cpp` that does the following:

1. **Read the Old Manifest**: Parse an existing CSV manifest located at `/home/user/manifest_v1.csv`. The CSV has the format `filepath,sha256sum` (where `filepath` is relative to `/home/user/project_data/`).
2. **Scan the Directory**: Recursively traverse the directory `/home/user/project_data/`.
3. **Compute Checksums**: Calculate the SHA-256 checksum for every file currently in `/home/user/project_data/`. You may shell out to the `sha256sum` command via `popen` or use any C++ approach you prefer.
4. **Identify Changes**: Compare the current files and checksums against `manifest_v1.csv`. A file is considered "changed" if it is newly added (not in the old manifest) or if its checksum has changed.
5. **Write an Incremental Binary Archive**: Pack all "changed" files into a custom binary archive at `/home/user/incremental.bin`. The binary format must strictly follow:
    - A 4-byte magic header: `ARCH` (ASCII).
    - For each changed file (sorted alphabetically by their relative path):
        - `path_length`: A 32-bit unsigned integer (little-endian) representing the length of the relative path string.
        - `path`: The relative path string (e.g., `src/main.cpp`), NOT null-terminated.
        - `file_size`: A 64-bit unsigned integer (little-endian) representing the file size in bytes.
        - `file_data`: The exact raw bytes of the file.
6. **Write a New Manifest**: Generate an updated manifest at `/home/user/manifest_v2.csv` containing all current files in `/home/user/project_data/` and their new SHA-256 checksums. The format must be exactly the same as `manifest_v1.csv` (`filepath,sha256sum`) and the lines must be sorted alphabetically by `filepath`.

Once you have written `archiver.cpp`, compile it (using `g++ -std=c++17 -O2 archiver.cpp -o archiver`) and run it to produce `/home/user/incremental.bin` and `/home/user/manifest_v2.csv`.