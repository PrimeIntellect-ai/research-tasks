You are tasked with writing a Python script `/home/user/extract_configs.py` to securely extract and process custom configuration archives used by our legacy configuration manager.

The archives use a custom binary format:
- `[2 bytes, unsigned little-endian]` - Number of file entries (N)
- For each entry:
  - `[1 byte, unsigned]` - Filename length (L)
  - `[L bytes]` - Filename string (ASCII)
  - `[4 bytes, unsigned little-endian]` - Compressed data length (C)
  - `[C bytes]` - Compressed data

The decompression algorithm for the data payload is as follows:
1. XOR every byte of the compressed data with a secret 8-bit integer key. 
2. The secret integer key is spoken in the audio file located at `/app/voice_memo.wav`. You must transcribe or listen to this audio to find the key (it is a single number spoken in English).
3. The XOR-decrypted bytes represent text encoded in UTF-16LE. Decode it to a Unicode string.
4. Encode the resulting string to UTF-8.

**Security Requirement (Zip-Slip Prevention):** 
To prevent path traversal attacks, if a filename contains the substring `../` or starts with `/`, you must **skip** this entry entirely. Do not process or output its contents.

**Concurrency Requirement:**
The configuration manager runs concurrently. Your script will be executed as:
`python3 /home/user/extract_configs.py <archive_file> <lock_file>`

Before processing the archive, your script must open `<lock_file>` and attempt to acquire an exclusive, non-blocking lock using `fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)`. 
- If the lock cannot be acquired (i.e., an exception is raised), your script must simply print `LOCKED` to STDOUT and exit with code 0.
- If the lock is acquired successfully, process the archive. For each **valid** file (that passes the zip-slip security check), print its UTF-8 decoded content to STDOUT (do not add any extra newlines or separators). 
- Keep the lock file open until processing is complete, then exit (the OS will release the lock, or you can release it explicitly).

Ensure your script is robust against malformed files and strictly follows the output format, as it will be evaluated against a rigorous automated fuzzing test.