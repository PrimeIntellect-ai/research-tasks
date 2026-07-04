As a technical writer, I regularly receive messy, nested documentation archives from our engineering team. I need you to organize the latest batch of files and generate a safe, atomic index using C++.

Here are your instructions:

1. **Extract the Nested Archives**:
   There is an archive located at `/home/user/docs_incoming.tar.gz`. When you extract it, you will find several `.zip` files. Extract all the Markdown (`.md`) files contained within those zip files into a new directory: `/home/user/processed_docs/`.

2. **Bulk Rename**:
   In `/home/user/processed_docs/`, sort the extracted `.md` files alphabetically by their original filenames. Rename them sequentially to `module_01.md`, `module_02.md`, `module_03.md`, etc., corresponding to their sorted alphabetical order.

3. **Symbolic Link**:
   Create a symbolic link at `/home/user/processed_docs/current_module.md` that points to the highest-numbered module file (e.g., if there are 4 files, it should point to `module_04.md`).

4. **Atomic Index Generation (C++)**:
   Write a C++ program at `/home/user/make_index.cpp`. This program must:
   - Read the `/home/user/processed_docs/` directory.
   - Collect the filenames of all regular `.md` files (do NOT include symbolic links like `current_module.md`).
   - Sort these filenames alphabetically.
   - Write the sorted filenames (one per line) to an index file. 
   - **Crucial Requirement**: You must use atomic writes to create the index file. Your C++ program must open and write to a temporary file (e.g., `index.tmp`), flush/close it, and then use the POSIX `rename()` function to atomically move it to `/home/user/processed_docs/index.txt`. This ensures no other processes read a partially written index.

Compile and run your C++ program so that `/home/user/processed_docs/index.txt` is successfully created.