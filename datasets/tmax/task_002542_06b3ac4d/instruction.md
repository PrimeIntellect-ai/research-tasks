You are an AI assistant helping a developer organize a chaotic, legacy project. 

The project has been handed to us as a nested archive located at `/home/user/legacy_project.tar.gz`. The original developers had a bad habit of hiding files by changing their extensions, and we need to sort them out based on their actual binary content (magic headers).

Your task is to:
1. Extract `/home/user/legacy_project.tar.gz`. Inside, you will find `inner.zip`. Unzip it to find `source_tree.tar`. Extract `source_tree.tar` into a new directory called `/home/user/project_root/`.
2. Write a C++17 program at `/home/user/sorter.cpp` that recursively traverses the `/home/user/project_root/` directory.
3. For every regular file encountered, the C++ program must use binary file I/O (e.g., `std::ifstream` in binary mode or memory-mapped I/O) to read exactly the first 4 bytes of the file (the magic number).
4. Based on the 4-byte magic number, identify and copy the file to a specific subdirectory within `/home/user/organized/` (create the directories if they do not exist), maintaining the original filename:
   - `\x89PNG` (Hex: `89 50 4E 47`): Copy to `/home/user/organized/png/`
   - `\x7FELF` (Hex: `7F 45 4C 46`): Copy to `/home/user/organized/elf/`
   - `PK\x03\x04` (Hex: `50 4B 03 04`): Copy to `/home/user/organized/zip/`
   - Any other files should be ignored.
5. The C++ program must generate a log file at `/home/user/report.log` containing one line for every matched file. The format of each line must be exactly:
   `[TYPE] /home/user/project_root/<relative_path_to_file>`
   Where `[TYPE]` is `PNG`, `ELF`, or `ZIP`. The lines in `/home/user/report.log` must be sorted alphabetically by the file path.
6. Compile the program using `g++ -std=c++17 -o /home/user/sorter /home/user/sorter.cpp` and run it to perform the sorting and logging.

Ensure the program gracefully handles files smaller than 4 bytes (ignore them) and leaves the original files in `/home/user/project_root/` untouched.