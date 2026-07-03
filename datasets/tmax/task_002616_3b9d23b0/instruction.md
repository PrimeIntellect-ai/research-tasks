You are a storage administrator managing a constrained disk environment. We have a large security video, `/app/surveillance.mp4`, that needs to be archived. We need to implement a custom concurrent archival tool to compress and store this video efficiently while ensuring the archiving process is safe from directory traversal vulnerabilities during extraction.

Your objective is to write a Python system consisting of two scripts: `archive.py` and `extract.py`.

1. **`archive.py` (Concurrent Chunking & Archiving):**
   - Extract frames from `/app/surveillance.mp4` as PNG images at 2 frames per second (fps) into a temporary directory.
   - Resize the frames to 50% of their original width and height to save space.
   - Divide the extracted frames evenly into 4 groups.
   - Spawn exactly 4 concurrent worker processes (using `multiprocessing`). Each worker must process its assigned group of frames.
   - For each frame, the worker compresses the image file using `zlib` or `gzip`.
   - Each worker must append its compressed frames to a single shared archive file located at `/home/user/video_archive.bin`.
   - **Crucial:** You must use POSIX file locking (e.g., `fcntl.flock`) when writing to `/home/user/video_archive.bin` to prevent race conditions and data corruption from the concurrent workers.
   - The archive format for each appended entry must be:
     `[Path Length (2 bytes, unsigned short)][File Path (UTF-8)][Data Length (4 bytes, unsigned int)][Compressed File Data]`
     *(Store the file path as just the filename, e.g., `frame_001.png`)*

2. **`extract.py` (Safe Extraction):**
   - Reads `/home/user/video_archive.bin` and decompresses the frames into `/home/user/restored_frames/`.
   - **Security Requirement:** Implement path sanitization to prevent "Zip Slip" directory traversal attacks. If an entry in the archive contains a path attempting to write outside the target directory (e.g., `../malicious.sh` or `/etc/passwd`), `extract.py` must skip that entry and print a warning, rather than extracting it.
   
Your solution will be evaluated by an automated script that:
1. Runs your `archive.py` to generate `/home/user/video_archive.bin`.
2. Measures the size of `/home/user/video_archive.bin` (it must be significantly smaller than the original video).
3. Appends a malicious entry to your archive to test your Zip Slip protection.
4. Runs your `extract.py` to restore the frames.
5. Computes the Structural Similarity Index (SSIM) between your restored, resized frames and the downsampled original frames.

**Success Criteria:**
- `/home/user/video_archive.bin` is successfully created using concurrent locked writes.
- Malicious paths are safely ignored by `extract.py`.
- The average SSIM of the restored frames compared to standard 50%-scaled frames is >= 0.90.
- The total size of the archive is less than 5 MB.

Ensure all dependencies (like `opencv-python` or `ffmpeg-python`, if you choose to use them) are installed via pip if needed, and write robust Python code.