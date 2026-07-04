You are a storage administrator managing disk space on a critical Linux server. The monitoring system has produced an automated alert image at `/app/disk_warning.png` and a binary memory dump at `/app/dump.bin`. 

Your goal is to parse these files and expose the results via a local HTTP service.

Perform the following steps:
1. **OCR the Alert**: Use `tesseract` to read the text from the image at `/app/disk_warning.png`. The image contains a volume identifier. Keep this string handy.
2. **Binary Header Extraction**: Extract the first 32 bytes of `/app/dump.bin` and save them to `/home/user/header.bin`.
3. **Chunking**: Read the remainder of `/app/dump.bin` (everything after the first 32 bytes) and split it into exactly 1 MB (1,048,576 bytes) chunks. Save these in `/home/user/chunks/` as `chunk_0.bin`, `chunk_1.bin`, etc. The final chunk will be smaller than 1 MB.
4. **Symlinks**: Create a directory `/home/user/active_links/`. Inside it, create symbolic links to each chunk (e.g., `link_0.bin` pointing to `/home/user/chunks/chunk_0.bin`, `link_1.bin` pointing to `/home/user/chunks/chunk_1.bin`, etc.).
5. **Serve the Data**: Write and run a Python script that starts an HTTP server on `127.0.0.1:8888`. 
   - Before starting to listen, the server MUST acquire an exclusive file lock (`fcntl.flock`) on `/home/user/server.lock`. It must hold this lock as long as the server is running.
   - When a `GET /volume` request is made, return the exact text extracted from the image (stripped of leading/trailing whitespace).
   - When a `GET /chunk/<id>` request is made (e.g., `/chunk/0`), read from the corresponding symlink in `/home/user/active_links/` and return the binary data.

Ensure your server runs continuously in the background and correctly serves these endpoints.