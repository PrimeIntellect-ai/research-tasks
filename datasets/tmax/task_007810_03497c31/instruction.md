You are an artifact manager tasked with curating incoming binary repositories. We frequently receive uncompressed tarballs containing binary artifacts. However, we have detected that some of these archives are deliberately crafted to exploit "Zip Slip" vulnerabilities—they contain files with malicious paths (e.g., paths starting with `/` or containing `../`) designed to overwrite system files during extraction.

Your task is to write a C++ program that manually parses an uncompressed tar archive, detects these malicious paths, and safely separates the artifacts without relying on external archive libraries (like `libarchive`). 

Here are the requirements:
1. Create a C++ source file at `/home/user/curator.cpp`.
2. The program must accept one command-line argument: the path to an uncompressed tar file.
3. It must read the archive binary format manually. Assume standard POSIX tar (ustar) format:
   - 512-byte headers.
   - File name at offset 0 (up to 100 bytes, null-terminated).
   - File size at offset 124 (12 bytes, null-terminated octal string).
   - The file data immediately follows the header and is padded to a multiple of 512 bytes.
   - The end of the archive is indicated by two consecutive 512-byte blocks of zeros.
4. For each file found in the tarball (indexed starting at 0):
   - Check if the file name is malicious. A file name is considered malicious if it starts with `/` or contains the substring `../`.
   - **If the file is safe:** Extract its binary contents to the directory `/home/user/safe_artifacts/`. All safe files in our incoming batches are guaranteed to be flat filenames (no directories, e.g., `artifact1.bin`).
   - **If the file is malicious:** 
     - Do NOT extract it to its specified path.
     - Extract its raw binary contents to a file named `/home/user/quarantine/<index>.bin` (where `<index>` is its 0-based index in the archive).
     - Append the exact malicious file path to `/home/user/quarantine.log` (one path per line).

Before running your program, you must ensure the directories `/home/user/safe_artifacts` and `/home/user/quarantine` exist. 

Compile your program using `g++ -O2 -o /home/user/curator /home/user/curator.cpp`.
An incoming test archive is located at `/home/user/incoming/artifacts.tar`. Run your compiled program on this file.