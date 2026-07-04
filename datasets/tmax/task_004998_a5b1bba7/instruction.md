You are tasked with helping a storage administrator handle custom, complex backup archives. The backups are often messy, containing deeply nested archives, files in legacy character encodings, and dangerous symlinks that have previously caused infinite loops in our backup parsers.

We use a proprietary deduplication hashing algorithm to index files. The hashing utility is provided as a pre-compiled binary at `/app/dedup_hash`. It is a stripped binary, but it works as a command-line tool: `/app/dedup_hash <filepath>` will print the hash of the file to standard output.

Your task is to write an HTTP service that dynamically processes incoming backup archives and generates a correct deduplication manifest.

**Service Requirements:**
1. Listen on `127.0.0.1:9090`.
2. Implement a single endpoint: `POST /api/v1/process_archive`. The request body will be raw binary data of a `.tar` archive.
3. When a request is received, the service must:
   a. Extract the `.tar` archive into a secure, isolated temporary directory.
   b. Recursively scan the extracted contents for nested archives (`.tar` or `.zip`). 
   c. If a nested archive is found, extract it into a subdirectory named exactly after the archive file, minus its extension (e.g., `data.zip` extracts into `data/`). After extraction, delete the nested archive file. Repeat this process until no nested archives remain.
   d. **Symlink handling**: The archives are known to contain malicious or accidental symlinks that point to parent directories, creating infinite loops. Your traversal logic must safely ignore infinite loops. Only process regular files and valid, non-looping directories.
   e. **Encoding conversion**: Any file with a `.txt` extension must be read, its character encoding detected (it could be UTF-16LE, Shift_JIS, ISO-8859-1, etc.), and rewritten in-place as UTF-8.
   f. **Hashing**: Run `/app/dedup_hash` on every final regular file.
4. The endpoint must return an `HTTP 200 OK` response with a JSON body representing the manifest:
```json
{
  "manifest": {
    "file1.txt": "<hash>",
    "folder/nested_file.bin": "<hash>"
  }
}
```
The keys in the `manifest` dictionary must be the relative paths of the files from the root of the initially extracted `.tar` archive.

Write and start this service so it runs continuously in the background. Do not hardcode responses; an automated verifier will send multiple novel archives to test your nested extraction, infinite loop prevention, and encoding conversion. You can use any programming language you prefer (Python, Node.js, etc.).