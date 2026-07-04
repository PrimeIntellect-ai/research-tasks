You are tasked with building a configuration and surveillance backup manager in Go. The system must collect configuration files, extract specific video frames, package them into an archive, and serve the result over an HTTP API. 

However, the configuration directories are known to contain infinite symlink loops created by a faulty legacy script, and your Go server must handle concurrent backup requests safely without data corruption.

Write a Go program that starts an HTTP server listening on `127.0.0.1:8080`.

The server must expose a single endpoint: `GET /generate-backup`.
When this endpoint is requested, the server must perform the following steps:

1. **Configuration Collection (Symlink Loop Evasion):**
   Traverse the directory `/app/configs/` to find all files with a `.conf` extension. 
   Warning: This directory contains symlink loops (e.g., symlinks pointing back to parent directories). Your Go code must safely detect and avoid infinite loops while traversing. You may only collect unique, regular `.conf` files.

2. **Video Frame Extraction:**
   There is a surveillance video located at `/app/surveillance.mp4`. 
   Extract exactly frame 30 and frame 60 from this video as JPEG images. You may invoke `ffmpeg` via Go's `os/exec` package. Name these extracted files `frame_30.jpg` and `frame_60.jpg`.

3. **Binary Header Extraction:**
   Read exactly the first 24 bytes of `/app/surveillance.mp4`. Save this binary data as a file named `header.bin` within your archive.

4. **Archive Creation & File Locking:**
   Package all collected `.conf` files (preserving their base names), `frame_30.jpg`, `frame_60.jpg`, and `header.bin` into a standard ZIP archive. 
   The ZIP archive must be written to disk at `/home/user/backup.zip`.
   Because the endpoint might be hit concurrently, you MUST use Go file locking (e.g., via `syscall.Flock`) or a Go `sync.Mutex` to ensure that only one request is generating and writing to `/home/user/backup.zip` at any given time.

5. **Response:**
   Once the ZIP file is safely written to disk, serve the contents of `/home/user/backup.zip` as the HTTP response body with an appropriate `application/zip` content type.

Requirements:
- Your Go program should be saved as `/home/user/server.go`.
- Run your Go server in the background so the terminal is free, or simply leave it running as the final step of your task.
- Ensure all file paths in the ZIP are at the root of the archive (no subdirectories).