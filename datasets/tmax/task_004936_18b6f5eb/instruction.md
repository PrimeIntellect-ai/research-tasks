You are tasked with organizing and parsing a massive dataset of binary project files for a high-performance backend system. 

We have a custom archiving library, `libdata-packer-1.0`, located at `/app/libdata-packer-1.0`. This library is designed to quickly bundle files into a custom `.pack` archive format. However, there are two issues:
1. The library has a critical bug: when instructed to follow symlinks during directory traversal, it enters infinite loops if symlinks point to parent directories. 
2. You need to write a C++ program that utilizes this library to parse, filter, and archive a large dataset, and it must be extremely fast.

**Your Objectives:**

1. **Fix the Vendored Library**:
   - Inspect the source code of `/app/libdata-packer-1.0`.
   - Fix the infinite loop bug in its recursive traversal logic. It *must* still follow directory symlinks, but it must actively detect and skip cyclic symlinks (e.g., by keeping track of visited filesystem locations using standard C++ filesystem equivalence or inode tracking).
   - Compile the fixed library as a static library (`libdatapacker.a`).

2. **Develop the Parsing Application**:
   - Write a C++ program at `/home/user/parser.cpp`.
   - Your program must recursively traverse the directory `/workspace/project_files`.
   - For every regular file encountered (including those reached via valid symlinks):
     - Check if the file starts with the 4-byte magic string `"DATA"`.
     - If it does, read the 32-bit unsigned little-endian integer at byte offset 4. Let this be `S`.
     - Extract exactly `S` bytes starting from byte offset 8.
     - Add this extracted chunk of data to the archive using the `libdata-packer-1.0` API, storing it under the same relative path it had in the source directory (e.g., `subdir/file.bin`).
   - Save the final archive to `/home/user/output.pack`.
   - **Performance Constraint**: To pass the rigorous automated tests, your program *must* use memory-mapped I/O (`mmap` via POSIX or a fast C++ equivalent) to read the source files. Standard stream reading (`std::ifstream`) will be too slow for the verifier's dataset.

3. **Compilation**:
   - Compile your program to `/home/user/fast_parser`, linking it against your fixed `libdata-packer.a`.

The automated verifier will replace `/workspace/project_files` with a massive, highly-linked, 500MB dataset. It will then execute `/home/user/fast_parser` and measure its execution time and output correctness.