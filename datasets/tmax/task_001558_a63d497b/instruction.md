You are tasked with building a configuration management and backup tracking service in C++. 

Our system configurations are stored in `/app/configs/`. Unfortunately, an old script created absolute and relative symlink loops inside this directory. We need a robust service that can traverse this directory, follow valid symlinks, but detect and abort on infinite symlink loops without crashing.

Additionally, our legacy system backed up historical configuration manifests by appending a custom steganographic payload to the end of a video file, located at `/app/config_history.mp4`.

You must write a C++ application (compiled to `/home/user/config_server`) that listens on **TCP port 8888** and handles the following text-based commands (each ending with a newline `\n`). The server should respond to each command and close the connection.

**Command 1: `BACKUP`**
- Traverse `/app/configs/`. Follow symlinks, but if a symlink loop is detected, skip that specific path.
- Collect all `.json` and `.txt` files.
- Pack them into a custom binary archive with the following format for each file:
  - 2 bytes (unsigned little-endian): Length of the relative file path (from `/app/configs/`)
  - N bytes: The relative file path string
  - 4 bytes (unsigned little-endian): File size in bytes
  - M bytes: The raw file contents
- After building this archive in memory, compress the entire binary blob using `zlib` (standard zlib compression).
- Send the raw compressed bytes back over the TCP socket.

**Command 2: `HISTORY`**
- The file `/app/config_history.mp4` is a standard video file, but it contains a custom payload appended to the very end of the file.
- Scan the file backwards or read through it to find the magic byte sequence: `CFGB`.
- Immediately following `CFGB` is a zlib-compressed JSON string containing the historical backup manifest.
- Decompress the payload to recover the JSON string.
- Send the raw JSON string back over the TCP socket.

**Command 3: `FRAME_HASH <N>`**
- Run `ffmpeg` to extract the `N`-th frame of `/app/config_history.mp4` (0-indexed).
- Calculate the SHA-256 hash of the extracted raw image data (in PPM format, extracted via `ffmpeg -i /app/config_history.mp4 -vf "select='eq(n\,<N>)'" -vframes 1 -f image2pipe -vcodec ppm -`).
- Send the hex-encoded SHA-256 hash string back over the socket.

**Constraints:**
- Use **C++** as your primary language for the server (`g++` and `zlib1g-dev` are available). You can use external tools like `ffmpeg` or `sha256sum` via `system()` or `popen()` for the frame extraction if you prefer.
- Run the server in the background so it is listening on port 8888 when you complete your task.
- Ensure your code properly handles the symlink loop located inside `/app/configs/` without infinite recursion.