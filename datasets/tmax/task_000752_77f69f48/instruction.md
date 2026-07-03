You are acting as a backup administrator managing legacy data. We have an old, custom binary backup format that is no longer supported, and we need to safely extract its contents, merge fragmented chunks, and expose the recovered files via an internal HTTP API. 

Here is what you need to do:

1. **Extract Configuration from Image**
There is a scanned administrative note at `/app/admin_notes.png`. Use OCR (e.g., `pytesseract`) to read the text from this image. It contains two vital pieces of information:
- `API_PORT`: The port number you must use for the HTTP server.
- `AUTH_TOKEN`: A secret key required to access the API.

2. **Process the Custom Archive**
We have a legacy backup file located at `/home/user/legacy_backup.bin`. 
The binary format is structured as follows:
- A 4-byte magic header: `BKUP`
- A sequence of file entries. Each entry consists of:
  - 2-byte unsigned integer (little-endian): Length of the file path (`L`).
  - `L` bytes: The file path (ASCII string).
  - 4-byte unsigned integer (little-endian): Size of the file data (`S`).
  - `S` bytes: The actual file data.

*Security Warning:* The legacy system had a flaw where it sometimes archived files with absolute paths or path traversal sequences (e.g., `../` or `/etc/`). This is a classic zip-slip vulnerability vector. 
You must parse this archive and extract the files into `/home/user/extracted_safe/`. **Crucially**, you must securely skip any entry whose path contains `..` or starts with `/`. Only extract safe, relative paths that do not attempt to escape the extraction directory.

3. **Merge Backup Chunks**
Inside the safe extracted files, you will find a directory `logs/` containing split files named `server.log.part1`, `server.log.part2`, etc. You must merge these in alphanumeric order into a single file at `/home/user/extracted_safe/logs/server_complete.log` and then recursively `tar` and `gzip` the entire `logs/` directory into `/home/user/extracted_safe/logs_archive.tar.gz`.

4. **Expose the Recovered Data via HTTP**
Write and start a Python HTTP server listening on `0.0.0.0` at the `API_PORT` you recovered from the image. 
- The server must handle `GET /download/<filepath>` requests, where `<filepath>` is the relative path of a file inside `/home/user/extracted_safe/`.
- The server MUST require an `Authorization` header in the format `Bearer <AUTH_TOKEN>` (using the token recovered from the image). If missing or invalid, return `401 Unauthorized`.
- If the file does not exist, return `404 Not Found`.
- If valid, return the file contents with a `200 OK` status.
- Ensure the server runs continuously in the background or foreground so it can be queried.