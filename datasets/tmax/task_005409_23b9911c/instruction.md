You are a storage administrator tasked with managing and optimizing disk space on a Linux server. The directory `/home/user/data` is consuming too much space due to duplicate files and leftover temporary files. 

You have been provided a CSV file at `/home/user/duplicates.csv` which lists known duplicate files. Each line in the CSV contains two absolute paths separated by a comma: `original_file,duplicate_file`.

Your task is to write a C program and perform some shell operations to consolidate the space and archive the results.

Step 1: Write a C program at `/home/user/dedup.c` that performs the following actions:
1. Opens and parses the CSV file `/home/user/duplicates.csv`.
2. For each line, deletes the `duplicate_file` and replaces it with a hard link pointing to the `original_file`.
3. Recursively traverses the `/home/user/data` directory and deletes any file that ends with the `.tmp` extension.
4. Keeps track of how many hard links were successfully created and how many `.tmp` files were successfully deleted.
5. Writes these counts to a JSON file at `/home/user/summary.json` in the exact following format:
   `{"links_created": X, "tmp_deleted": Y}` (where X and Y are the integer counts).

Step 2: Compile your C program and run it to process the files.

Step 3: After the C program finishes executing successfully, use standard shell utilities to create a gzip-compressed tar archive of the entire optimized `/home/user/data` directory. Save this archive at `/home/user/data_archive.tar.gz`.

Ensure your C code handles file paths and operations securely and correctly. You may use standard C library headers and POSIX APIs (e.g., `<unistd.h>`, `<dirent.h>`, `<sys/stat.h>`).