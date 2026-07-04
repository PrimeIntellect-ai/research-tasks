I need you to write a Python script that acts as a secure unpacker for a custom binary archive format used in our project. We have a file located at `/home/user/archives/data.binpack` which contains multiple file entries.

Your script must be saved to `/home/user/unpack.py` and when executed, it should extract the contents of `/home/user/archives/data.binpack` into the directory `/home/user/project_outbox/`.

Here are the strict technical requirements for the extraction:

1. **Memory-Mapped I/O**: You must use Python's `mmap` module to read the `.binpack` file. Do not read the entire file into standard memory at once.
2. **Binary Header Format Extraction**: The `.binpack` file contains concatenated entries. Each entry has the following exact structure:
   - `Path Length` (2 bytes): An unsigned short (little-endian) indicating the size of the file path string in bytes.
   - `File Path`: The relative file path encoded in **UTF-16-LE**.
   - `Payload Size` (4 bytes): An unsigned int (little-endian) indicating the size of the file payload in bytes.
   - `Payload`: The actual file content, which is text encoded in **ISO-8859-1**.
3. **Character Encoding Conversion**: When saving the extracted files to disk, you must convert the payload from ISO-8859-1 to **UTF-8**.
4. **Security (Zip-Slip Prevention)**: Our custom format is vulnerable to path traversal attacks (e.g., paths trying to escape the destination directory using `../`). 
   - Before writing any file, securely resolve the path.
   - If a file path attempts to write outside of the base directory `/home/user/project_outbox/`, **do not extract it**.
   - Instead, append the original, unextracted malicious file path string (e.g., `../../etc/passwd`) to a log file located at `/home/user/security.log`, one path per line.

Create the target directory `/home/user/project_outbox/` if it doesn't exist, and run your script to process the archive.