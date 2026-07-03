You are acting as a technical assistant for a technical writer. The writer has a large, disorganized repository of documentation located at `/home/user/docs_repo`. The repository contains various documentation files, including images, markdown files, and draft files.

Your task is to create a documentation indexing tool in C that traverses this repository, generates a checksum for each finalized file, and produces a sorted manifest. 

Here are the specific requirements:

1. **Write the Indexer:** 
   Create a C program at `/home/user/doc_indexer.c`. This program must:
   - Accept a single command-line argument: the absolute path to the directory to index.
   - Recursively traverse the given directory.
   - Ignore any files that end with the `.draft` extension (these are works in progress).
   - Ignore directories themselves (only process regular files).
   - For every valid file, compute its SHA-256 checksum. You may use `popen` to call the system's `sha256sum` utility from within your C code.
   - Print the result to standard output in the exact format: `<SHA256_HASH> <relative_path_from_target_dir>`
   - The relative path must start with `./`. For example, if the target dir is `/home/user/docs_repo`, a file at `/home/user/docs_repo/v1/intro.md` should be output as `./v1/intro.md`.

2. **Compile the Indexer:**
   Compile your C program into an executable located at `/home/user/doc_indexer`. Standard GCC is available.

3. **Generate the Manifest:**
   Run your compiled `/home/user/doc_indexer` tool against the `/home/user/docs_repo` directory. 
   Using standard stream redirection and shell piping, sort the output of your program alphabetically by the SHA-256 hash (the first column) and save the final output to `/home/user/doc_manifest.txt`.

Ensure your C program robustly handles standard recursive directory traversal (e.g., ignoring `.` and `..` directories).