I am a researcher managing a large repository of dataset archives submitted by various third-party collaborators. Recently, we discovered that some of the submitted `.zip` archives are malformed or potentially malicious. Specifically, they contain entries with path traversal sequences (like `../`) or absolute paths, attempting to exploit a "Zip Slip" vulnerability to overwrite files outside the intended extraction directory. 

I need you to write a Go program to safely extract these datasets while identifying the malicious files.

Here are the requirements:
1. The submitted archives are located in `/home/user/datasets/`. You must recursively traverse this directory to find all `.zip` files.
2. For each `.zip` file found, your Go program must read the archive's headers and entries.
3. You must extract the contents of each archive into `/home/user/clean_data/<archive_filename_without_extension>/`.
4. **Security Check (Zip Slip protection)**: Before extracting any file from an archive, you must calculate its intended absolute extraction path. If the resolved absolute path does not fall within the specific target directory for that archive (i.e., `/home/user/clean_data/<archive_filename_without_extension>/`), you must **not** extract that file.
5. Whenever a malicious or malformed file entry is detected in an archive, log it to `/home/user/malicious.log`. 
6. The format of `/home/user/malicious.log` must be exactly one entry per line, formatted as: `[<zip_filename>] <malicious_entry_path>` (e.g., `[dataset3.zip] ../../../etc/passwd`). Do not include the full path to the zip file in the brackets, just the basename. Sort the lines alphabetically in the final log file.
7. Safe files within the same archive should still be extracted normally.

You must write your solution in a file named `/home/user/extractor.go`, compile it, and run it to process the datasets and generate the log and extracted files.