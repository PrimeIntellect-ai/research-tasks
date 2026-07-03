You are an AI assistant helping a technical writer organize a set of legacy documentation files. 

The writer has an archive of old documentation located at `/home/user/legacy_docs.tar.gz`. The archive contains a single top-level directory named `docs/` with various nested subdirectories and `.txt` files.

These text files contain metadata tags for the author and date, but the formatting is inconsistent due to spaces. The tags look like `%% AUTHOR : Alice %%` or `%%DATE: 2020-01-01%%`.

Your task is to:
1. Extract the `/home/user/legacy_docs.tar.gz` archive into `/home/user/`.
2. Use standard command-line text transformation tools (like `sed` or `awk`) to normalize the metadata tags in all `.txt` files in the extracted `docs/` directory. Specifically, remove any spaces between `%%`, `AUTHOR`, `:`, and the actual name, and similarly for `DATE`. So `%% AUTHOR : Alice %%` must become `%%AUTHOR:Alice %%` (do not alter spaces *after* the value before the closing `%%`, just strip spaces up to and including the space right after the colon). Specifically, the target formats to match and replace are:
   - Normalize `%%[spaces]AUTHOR[spaces]:[spaces]` to `%%AUTHOR:`
   - Normalize `%%[spaces]DATE[spaces]:[spaces]` to `%%DATE:`
3. Write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`. The program should accept a single file path as a command-line argument. It must read the file, extract the author name (everything after `%%AUTHOR:` up to the next `%` or space) and the date (everything after `%%DATE:` up to the next `%` or space), and print a single line to standard output in the format: `filepath,author,date`. If a file is missing one of the tags, output `UNKNOWN` for that field.
4. Run your compiled C program on every `.txt` file inside the `docs/` directory (including all subdirectories). 
5. Collect the output into a single CSV file at `/home/user/metadata.csv`. Sort the lines of the CSV file alphabetically by the `filepath` column.
6. Finally, package the normalized `docs/` directory and the `metadata.csv` file into a new compressed archive located at `/home/user/processed_docs.tar.gz`.

Ensure your C program is robust enough to handle the file paths correctly. Do not use absolute paths for the `filepath` in the CSV; use the relative path starting with `docs/...` exactly as it appears when traversing the directory from `/home/user/`.