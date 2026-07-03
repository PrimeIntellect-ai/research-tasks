You are an AI assistant helping a technical writer organize a deeply nested, messy legacy documentation archive. 

I have a directory at `/home/user/docs_raw` that contains markdown documentation files (`.md`). Over the years, authors created a chaotic web of symlinks within this directory, some of which form infinite loops (e.g., `linkA` points to `linkB` which points to `linkA`). 

Your task is to write a C program, a shell script, and run them to produce a clean, flattened archive of these documents.

Please follow these exact phases:

**Phase 1: The C Flattener**
Write a C program at `/home/user/flattener.c` and compile it to `/home/user/flattener`.
This program must:
1. Accept two arguments: a source directory (`/home/user/docs_raw`) and a destination directory (`/home/user/docs_flat`).
2. Read all files and symlinks in the source directory (you do not need to recurse into subdirectories, just the top-level directory).
3. Safely resolve symlinks. If a symlink forms an infinite loop or is broken, print a warning to `stdout` and skip it.
4. For all valid regular files (and valid symlinks pointing to regular files), copy their contents to the destination directory, keeping the original file/symlink name.
5. **Crucial:** You must use atomic writes and temporary file management for the copying process. Write the contents to a temporary file in the destination directory (e.g., `filename.md.tmp`) and then use the `rename()` system call to atomically move it to its final name (`filename.md`).

**Phase 2: Bulk Renaming and Macro Text Editing**
Once the files are safely in `/home/user/docs_flat`, write a bash script at `/home/user/organizer.sh` and execute it. The script must:
1. Iterate over all `.md` files in `/home/user/docs_flat`.
2. Every valid documentation file contains a line formatted exactly like this: `DOC_ID: <number>` (e.g., `DOC_ID: 042`). Extract this number.
3. Bulk rename the files by prepending the extracted `DOC_ID` and an underscore to the filename (e.g., `intro.md` becomes `042_intro.md`). If a file doesn't have a `DOC_ID`, leave its name unchanged.
4. Perform a bulk text edit using `sed` or `awk`: append the string `ARCHIVED_2024_TECH_WRITER` as a new line at the very end of every file in `/home/user/docs_flat`.

**Phase 3: Archiving**
Finally, bundle the processed files into a compressed tarball at `/home/user/final_docs.tar.gz`. The tarball should contain the flattened, renamed files at the root of the archive (do not include the `docs_flat` directory structure itself in the tarball).

Constraints:
- Do not use external libraries in C other than the standard POSIX and C standard libraries.
- Ensure the C program exits with code 0 on success.
- Ensure no loop files make it into the final archive.