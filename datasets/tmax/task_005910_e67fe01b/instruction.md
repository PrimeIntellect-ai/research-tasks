You are an AI assistant helping a technical writer organize a set of legacy documentation files before migrating them to a new platform. 

The writer has provided you with an archive `/home/user/legacy_docs.tar.gz` containing hundreds of documentation text files (`.txt`) scattered across a deeply nested directory structure. Along with the archive, there is a CSV index file at `/home/user/doc_index.csv`.

The CSV file uses the format: `original_filename,new_filename,section,status`
(Note: the CSV has a header row, and `original_filename` does not include the path, just the basename).

Your task is to:
1. Extract `/home/user/legacy_docs.tar.gz`.
2. Write a C program named `/home/user/doc_parser.c` that parses `/home/user/doc_index.csv`. 
3. Your C program must find every file listed in the CSV where the `status` column is exactly the string `approved`.
4. For each `approved` file, the program must locate the file within the extracted directory tree and rename it to its corresponding `new_filename` (appending `.txt` to the new filename).
5. All renamed `approved` files must be moved (flattened, disregarding their original nested folder structure) into a new directory: `/home/user/approved_docs/`.
6. Finally, create a new archive at `/home/user/final_docs.tar.gz` containing ONLY the contents of the `approved_docs` directory (do not include the parent `approved_docs` directory itself in the archive paths, just the files).

Requirements:
- You MUST write and use a C program (`/home/user/doc_parser.c`) to parse the CSV file. You can compile it with standard `gcc`.
- Files that are NOT `approved` (e.g., `draft` or `deprecated`), or files not listed in the CSV, must be completely ignored.
- You may use standard shell commands (like `tar`, `mkdir`, `find`) in conjunction with your C program or by calling them via `system()` within C.