You are acting as a storage administrator for a custom Video Management System (VMS). Disk space is running out on the primary logging drive because the system constantly extracts uncompressed raw frames from video feeds for analysis. 

Your task is to build a C-based storage daemon that watches for new frames, compresses them into a single custom archive file on the fly using a custom compression algorithm, and serves the uncompressed frames over a TCP socket when requested.

Here is the step-by-step workflow:

1. **Frame Extraction Spool:**
   Create a directory at `/home/user/spool/`. 
   You have a video file located at `/app/cctv.mp4`. To simulate the live video feed extraction, write a simple bash script that uses `ffmpeg` to extract the first 30 frames of this video at a rate of 1 frame per second. The output format must be uncompressed PGM (Portable Graymap). The output files must be written into `/home/user/spool/` with the naming pattern `frame_%03d.pgm` (e.g., `frame_001.pgm`).

2. **The Storage Daemon (`storage_daemon.c`):**
   Write a C program that performs the following duties simultaneously:
   
   **A. File Watching & Archiving:**
   - Use `inotify` to monitor `/home/user/spool/` for new files (specifically waiting for them to be fully written, e.g., `IN_CLOSE_WRITE`).
   - When a new `.pgm` file is detected, read its contents.
   - Compress the file's contents using a **custom Run-Length Encoding (RLE)** algorithm that you must implement from scratch. Do not use external compression libraries like zlib.
   - Append the compressed data (along with any metadata needed to identify and extract it later, like the original filename and sizes) to a single custom archive file located at `/home/user/video_archive.bin`.
   - Once successfully archived, the daemon must immediately delete the original `.pgm` file from `/home/user/spool/` to save disk space.

   **B. TCP Retrieval Service:**
   - The daemon must start a TCP server listening on `127.0.0.1:8888`.
   - When a client connects and sends a request in the exact format `FETCH <filename>\n` (e.g., `FETCH frame_015.pgm\n`), the server must:
     1. Locate the requested frame within `/home/user/video_archive.bin`.
     2. Decompress the custom RLE data back to its original PGM form.
     3. Send the exact, uncompressed bytes of the original PGM file back over the TCP socket.
     4. Close the client connection.
   - If a requested frame does not exist, send `ERROR\n` and close the connection.

3. **Execution:**
   - Compile and start your C daemon in the background.
   - Run your ffmpeg extraction script so the daemon can process the files as they arrive.
   - Leave the daemon running in the background when you complete the task.

**Constraints:**
- The total size of `/home/user/video_archive.bin` must be strictly smaller than the combined size of the raw PGM files, proving your RLE implementation works.
- The retrieved PGM files over the TCP socket must be a perfect byte-for-byte match with the originals.
- Your C code must be robust enough to handle the race condition of reading a file right after `ffmpeg` finishes writing it.