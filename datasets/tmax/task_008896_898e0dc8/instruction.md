You are helping a researcher organize and secure a newly acquired dataset. The dataset was provided as a tar archive located at `/home/user/dataset.tar`. However, you suspect that this archive might have been tampered with and contains a "Zip Slip" payload—files with paths that attempt to overwrite system files outside the extraction directory (e.g., paths starting with `/` or containing `../`).

Perform the following steps:

1. Write a C++ program at `/home/user/filter_archive.cpp` and compile it to `/home/user/filter_archive`. 
   - The program must read a list of file paths from standard input (one path per line).
   - It must evaluate each path and print it to standard output ONLY if it is "safe".
   - A path is considered "unsafe" (and should be ignored) if it starts with a forward slash `/` OR if it contains `../` as a directory component (or `..` at the end of the path).
   
2. List the contents of `/home/user/dataset.tar` using `tar -tf` and pipe the output through your `/home/user/filter_archive` program. Save the safe paths to `/home/user/safe_files.txt`.

3. Extract ONLY the safe files from `/home/user/dataset.tar` into the directory `/home/user/extracted/` (create this directory if it doesn't exist) using the list generated in the previous step.

4. Bulk rename all files inside `/home/user/extracted/` (and its subdirectories) by prepending `clean_` to the filename. (e.g., `data.csv` becomes `clean_data.csv`, `subdir/info.txt` becomes `subdir/clean_info.txt`). 

5. Create a listed-incremental backup of the `/home/user/extracted/` directory using `tar`. 
   - The archive must be named `/home/user/backup1.tar`.
   - The snapshot file must be named `/home/user/backup.snar`.

Ensure all operations are completed and the C++ source file, the compiled executable, the text file, the extracted directory, and the backup archives are present at the specified paths.