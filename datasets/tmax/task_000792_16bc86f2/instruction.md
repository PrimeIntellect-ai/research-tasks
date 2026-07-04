You have been hired to recover data from a misconfigured backup system. The previous administrator created a bizarre archiving script that stored motion-event metadata in deeply nested archives with circular symlinks. 

There are two critical files on your system:
1. `/app/security_cam.mp4` - A raw video file recovered from the security system.
2. `/app/backup_root.tar.gz` - A compressed archive containing the backup directory structure and metadata chunks.

Your objective is to traverse the broken backup, reconstruct the motion-event metadata, and expose an HTTP API to serve video frame analysis.

**Step 1: Parse the Archive**
Extract `/app/backup_root.tar.gz`. The extracted directory structure contains several subdirectories, regular files, and symbolic links. Some of the symbolic links point backwards, creating infinite loops.
You must carefully traverse the directory tree (avoiding infinite loops) and locate all files matching the pattern `chunk_*.bin.gz`. 
Extract and decompress these files. When concatenated in numerical order based on their filenames (e.g., chunk_1, chunk_2...), they form a single plain-text list of floating-point timestamps (one per line). These are the times (in seconds) when motion was detected.

**Step 2: Video Analysis and API Service**
Create and start an HTTP server listening on `127.0.0.1:9090`. The server must implement the following endpoints:

*   `GET /ping`
    *   **Response:** Plain text `pong`.
*   `GET /api/timestamps`
    *   **Response:** A comma-separated list of all the motion timestamps recovered from the chunks, sorted in ascending numerical order.
*   `GET /api/frame_brightness?time=<float>`
    *   **Behavior:** The server must extract the exact video frame from `/app/security_cam.mp4` at the given timestamp in seconds. Extract the frame using standard 8-bit grayscale format (`gray`). Calculate the average pixel brightness of this frame (the sum of all pixel values divided by the total number of pixels, rounded down to the nearest integer using the floor function).
    *   **Response:** Plain text integer representing the average brightness.

**Requirements & Constraints:**
*   You may write your scripts in any programming language available in a standard Linux environment (Python, Node, Bash, etc.).
*   Ensure your HTTP server binds specifically to `127.0.0.1:9090`.
*   Run the server in the background and print `SERVICE_READY` to standard output when your server is fully initialized and ready to accept requests.
*   Make sure you account for the infinite directory loops when traversing the extracted archive, or your script will hang.