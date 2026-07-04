You are a developer tasked with cleaning up a legacy project directory that has been poorly archived and contains corrupted filesystem links. 

Your objective is to recombine a multi-part archive, write a custom C utility to safely traverse the extracted filesystem (which contains infinite symlink loops), index the unique files, and create a clean backup archive.

Here are the precise steps you must follow:

1. **Recombine and Extract the Archive:**
   In `/home/user/legacy_archives/`, there is a split tarball archive named `backup.tar.gz.part-aa` and `backup.tar.gz.part-ab`.
   Recombine these parts and extract the resulting tarball into the directory `/home/user/extracted_project/`. 
   *Note: This extracted directory structure contains several nested folders, regular files, symlinks to files, and unfortunately, circular symlinks that point back to their own parent directories.*

2. **Write a Safe Directory Traversal Tool in C:**
   Standard tools like `find` might get stuck or behave unexpectedly with the specific loops in this project. You must write a C program at `/home/user/safewalk.c` that does the following:
   - Takes a starting directory path as its first command-line argument.
   - Recursively traverses the directory tree.
   - Follows symlinks.
   - **Crucially:** It must keep track of visited files and directories (e.g., by tracking the `dev` and `ino` fields from `stat()`) to prevent infinite loops and to ensure no regular file is processed more than once, even if multiple symlinks point to it.
   - Whenever it encounters a *unique* regular file, it should resolve its absolute path (using `realpath()`) and print it to standard output in the following format:
     `<absolute_path> <file_size_in_bytes>`
   - Skip missing or broken symlinks.

3. **Compile and Run the Tool:**
   Compile your C program. Run it with `/home/user/extracted_project/` as the target directory. 
   Sort the output alphabetically by the absolute path and save the result exactly to `/home/user/final_index.txt`.

4. **Create a Clean Archive:**
   Using the list of unique absolute paths generated in the previous step (extracting just the path part from `/home/user/final_index.txt`), create a new, flattened, uncompressed tar archive at `/home/user/clean_backup.tar`. 
   You must use the exact absolute paths so that the files in the archive are stored under their absolute path directory structure (e.g., `home/user/extracted_project/...`).

Ensure your C code is robust and handles standard system calls correctly.