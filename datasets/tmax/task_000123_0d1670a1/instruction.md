You are acting as an artifact manager curating a binary repository. 

There is a nested directory structure containing various artifact files at `/home/user/raw_repo`. Your job is to locate specific candidate binaries, verify their headers, and generate a curated index.

Please complete the following steps:
1. Find all files within `/home/user/raw_repo` (and its subdirectories) that meet the following metadata criteria:
   - They have the executable permission bit set for the owner.
   - Their size is greater than 50 KB.

2. Write a C++ program at `/home/user/filter_elf.cpp` and compile it to `/home/user/filter_elf`. This program must:
   - Read absolute file paths from standard input (one path per line).
   - Open each file and read its first 4 bytes.
   - Verify if the file has a standard ELF magic number (`0x7F`, `'E'`, `'L'`, `'F'`).
   - If it is a valid ELF file, print the original file path to standard output.

3. Pipe the paths found in step 1 into your C++ program. Then, pipe the output of your program through `awk` or `sed` to extract *only the base filename* (strip out the directory path) and append the suffix `-curated` to each filename.

4. Redirect this final transformed output to `/home/user/curated_list.txt`. Sort the final text file alphabetically.

Ensure your compiled C++ program is exactly at `/home/user/filter_elf` and your final output file is exactly at `/home/user/curated_list.txt`.