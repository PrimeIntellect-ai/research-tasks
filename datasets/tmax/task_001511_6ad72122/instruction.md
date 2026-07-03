You are tasked with recovering and migrating a set of legacy configuration files, then serving them via a custom C-based API for a configuration management system.

**Stage 1: Recover the Authorization Key from Video**
You have been provided with a video artifact at `/app/system_monitor.mp4`. This video contains a hidden 15-character authorization key.
- The video plays at 1 frame per second for exactly 120 frames.
- In each frame, the top-left 10x10 pixel block is either pure white (representing a binary `1`) or pure black (representing a binary `0`).
- Extract these 120 bits (frame 0 is the most significant bit of the first byte, frame 7 is the least significant bit, etc.). 
- Convert the 120 bits into 15 ASCII characters. This is the `AUTH_KEY`.

**Stage 2: Archive Processing and Text Editing**
There is a nested archive at `/app/legacy_configs.tar`. It contains multiple compressed archives (`.tar.gz`, `.zip`, etc.) which in turn contain `.conf` files.
1. Recursively extract all `.conf` files into `/home/user/extracted_configs/`.
2. Perform large-scale text editing on all extracted `.conf` files:
   - Find all instances of `server_ip=192.168.1.X` (where X is any number between 1 and 255) and replace them with `server_ip=10.0.0.X`.
   - Find all instances of `mode=legacy` and replace them with `mode=modern`.

**Stage 3: Configuration Manager Service (C Program)**
Write a C program at `/home/user/config_server.c` that compiles to `/home/user/config_server`.
- The program must act as an HTTP server listening on `127.0.0.1:8080`.
- It must handle incoming `GET /manifest` requests.
- **Authentication**: If the HTTP request does NOT contain the header `X-Auth-Key: <AUTH_KEY>` (the exact string recovered from the video), the server must return `401 Unauthorized`.
- **Manifest Generation**: If authenticated, the server must dynamically compute the SHA-256 checksums of all `.conf` files currently in `/home/user/extracted_configs/` (ignoring subdirectories, just flat file names).
- The response to `GET /manifest` must be `200 OK` with a plaintext body formatted exactly as:
  `<filename>:<sha256_hex>` (sorted alphabetically by filename, one per line).

**Instructions:**
- You may use standard Linux utilities (ffmpeg, sed, awk, find, etc.) for extraction and text processing.
- The HTTP server must be written in C. You may use raw sockets, `libmicrohttpd`, or any standard C library available in the environment.
- Start your server in the background and leave it running.