I am a developer organizing some older project files that were archived using a custom, rudimentary archiving format called CAZ (Custom Archive Zip). Recently, I discovered that the archiver tool had a flaw: it allowed "Zip Slip" vulnerabilities by including relative path traversals (like `../`) or absolute paths (like `/etc/passwd`) in the archived file paths.

I need you to write a C program that acts as a safe extractor for these `.caz` archives. 

Here are the details of the `.caz` binary format (all multi-byte integers are Little Endian):
1. **Magic Header**: The file always starts with the 4 ASCII characters `CAZ1`.
2. **File Count**: An unsigned 32-bit integer representing the number of files in the archive.
3. **File Entries**: For each file, the following sequence appears:
   - **Path Length**: An unsigned 16-bit integer representing the length of the file path.
   - **File Path**: The path string (not null-terminated, exactly "Path Length" bytes long).
   - **File Size**: An unsigned 32-bit integer representing the size of the file data.
   - **File Data**: The raw binary data of the file (exactly "File Size" bytes long).

Your task:
1. Write a C program at `/home/user/extractor.c`.
2. The program must compile successfully using `gcc /home/user/extractor.c -o /home/user/extractor`.
3. The program must take two command-line arguments: the path to the `.caz` archive, and the destination directory where files should be extracted. Example: `./extractor /home/user/project.caz /home/user/extracted/`
4. **Security Requirement**: You must prevent Zip Slip vulnerabilities. If a file path inside the archive starts with `/`, or contains the substring `../`, the program must **reject** the file and completely skip extracting its data. 
5. For valid paths, the program should create the necessary subdirectories in the destination directory and write the file data. (You may assume safe paths do not contain tricky subdirectories requiring complex resolution, just standard relative structures like `src/main.c`).
6. **Logging Requirement**: Your program must output a log of its actions to a file named `extraction.log` inside the destination directory (e.g., `/home/user/extracted/extraction.log`).
   - For every file in the archive, write exactly one line to the log.
   - If the file is extracted safely: `EXTRACTED: <original_path>`
   - If the file is rejected due to security rules: `REJECTED: <original_path>`
7. Run your compiled extractor on the provided archive `/home/user/project.caz` and extract it to `/home/user/safe_output`.

Please write the code, compile it, and execute it to safely extract `/home/user/project.caz`.