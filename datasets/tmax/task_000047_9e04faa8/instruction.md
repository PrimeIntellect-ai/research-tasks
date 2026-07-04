You are an AI assistant helping a data researcher parse a custom legacy dataset archive. 

The researcher received a custom binary archive file located at `/home/user/dataset.bin`. However, they suspect the archive was poorly generated and might contain malicious paths attempting a "zip slip" attack (extracting files outside the intended destination directory).

Your task is to write and execute a Go program (save it as `/home/user/extractor.go`) that safely extracts this custom binary archive into the directory `/home/user/extracted/`.

**Archive Format Specification:**
The file `/home/user/dataset.bin` is a binary file containing a sequence of file records. 
1. The file starts with a 4-byte magic signature: `DATA` (ASCII).
2. Immediately following the signature are the file records. Each record consists of:
   - `path_length`: A 16-bit unsigned integer (Little-Endian) representing the length of the file path.
   - `path`: A UTF-8 string of `path_length` bytes representing the relative path where the file should be extracted.
   - `content_length`: A 32-bit unsigned integer (Little-Endian) representing the size of the file content in bytes.
   - `content`: The actual file data (raw bytes of `content_length` size).

**Requirements for the Go Program:**
1. **Parse the binary file:** Read `/home/user/dataset.bin` according to the format above.
2. **Prevent Zip Slip:** Before extracting a file, verify that its destination path securely falls within `/home/user/extracted/`. 
   - You must detect paths that try to escape the target directory (e.g., using `../` components).
3. **Extract safe files:** If a file is safe, extract it to its intended location inside `/home/user/extracted/`, creating any necessary subdirectories.
4. **Log malicious files:** If a file path attempts to escape the `/home/user/extracted/` directory, DO NOT extract it. Instead, append the exact `path` string (as read from the archive) to `/home/user/malicious.log`, one path per line.

Once you have written the script, compile and run it to perform the extraction.

**Success Criteria:**
- The `/home/user/extracted/` directory contains only the safe files with their correct contents.
- No files are written outside of `/home/user/extracted/`.
- The `/home/user/malicious.log` file contains exactly the original path strings of the skipped files, separated by newlines.