You are an AI assistant helping a technical writer organize a massive dump of legacy documentation.

The documentation has been delivered to you in a nested archive located at `/home/user/incoming/legacy_docs.tar.gz`. 
Your goal is to extract, filter, and reorganize these files using standard Linux commands and a custom C program.

Here are your instructions:
1. **Extraction**: Extract the contents of `/home/user/incoming/legacy_docs.tar.gz`. Inside, you will find a CSV file named `metadata.csv` and a zip archive named `raw_docs.zip`. Extract `raw_docs.zip` as well.
2. **Filtering**: The extracted documentation contains many empty or placeholder files. Find all `.md` files that are strictly **greater than 50 bytes** in size. Save the base filenames (just the names, no paths) of these valid files into a text file at `/home/user/valid_files.txt`.
3. **Data Parsing & Renaming (C Program)**: 
   Write a C program at `/home/user/organizer.c` (and compile it to `/home/user/organizer`) that does the following:
   - Reads `metadata.csv`. The CSV has no header and contains four columns: `original_filename,department,document_title,revision_number` (you can assume no fields contain commas).
   - Reads `/home/user/valid_files.txt`.
   - For every file listed in `valid_files.txt` that also has an entry in `metadata.csv`, the program must:
     a. Create a directory for the `department` inside `/home/user/organized_docs/` (e.g., `/home/user/organized_docs/Engineering/`).
     b. Move and rename the file from its extracted location to the new department directory. The new filename must follow the format: `[document_title]_r[revision_number].md`.
   - Any file not in `valid_files.txt` or not in the CSV should be ignored.
4. **Verification**: After your C program has executed, run a command to list all files in `/home/user/organized_docs/` (recursively, printing only the file paths relative to `/home/user/organized_docs/`, sorted alphabetically) and save this output to `/home/user/final_inventory.txt`.

Constraints:
- Do not use external C libraries for CSV parsing (standard library `<stdio.h>`, `<string.h>`, etc., are fine).
- Ensure your C program handles directory creation (e.g., using `mkdir` from `<sys/stat.h>`).
- You may use any standard shell commands for extraction, compilation, and generating the final inventory.