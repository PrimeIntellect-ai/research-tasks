I am a technical writer working on unifying our video tutorials and written documentation. I need you to set up a workspace, process a screencast, organize some backup files, and write a custom binary parser in C++ to handle our legacy timestamp format.

Please complete the following steps in order:

**Stage 1: Video Processing and Manifest Generation**
There is a video tutorial located at `/app/screencast.mp4`. 
1. Create a directory `/home/user/frames/`.
2. Using `ffmpeg`, extract one frame every 5 seconds from the video and save them as PNGs in `/home/user/frames/` with the naming pattern `frame_001.png`, `frame_002.png`, etc.
3. Generate a SHA-256 checksum manifest of these frames and save it to `/home/user/frames_manifest.txt`. The format should be exactly the output of the `sha256sum` command (e.g., `<hash>  frame_001.png`). Run this command from within the `/home/user/frames/` directory so the paths are relative.

**Stage 2: Differential Document Backup Search**
I have an archive of raw markdown files in `/home/user/docs_raw/` (which you can assume exists or you should test your workflow against).
1. Create `/home/user/filtered_docs/`.
2. Find all `.md` files in `/home/user/docs_raw/` that are strictly larger than 512 bytes, and copy them into `/home/user/filtered_docs/`.

**Stage 3: Legacy Binary Format Parser (C++)**
Our old documentation system used a proprietary binary format (`.tdoc`) to map video timestamps to documentation metadata. I need a C++ program to parse these files and output text.

Write a C++ program at `/home/user/tdoc_parser.cpp` and compile it to `/home/user/tdoc_parser` (using `g++ -O3 -std=c++17`).

The program must take exactly one argument: the path to a `.tdoc` file.
It should read the binary file and output text to `stdout`.

**Format Specification for `.tdoc`:**
*   **Magic Header:** 4 bytes, must be exactly "TDOC" (ASCII).
*   **Version:** 1 byte, unsigned. Must be exactly `1`.
*   **Record Count:** 2 bytes, little-endian unsigned integer.
*   **Records:** For each record (up to the Record Count):
    *   **Timestamp:** 4 bytes, little-endian unsigned integer (represents seconds).
    *   **Doc ID:** 2 bytes, little-endian unsigned integer.
    *   **Content Length:** 2 bytes, little-endian unsigned integer.
    *   **Content:** `Content Length` bytes of ASCII text.

**Parsing Rules:**
*   If the file cannot be opened, is shorter than 7 bytes, fails the magic header check, or fails the version check, the program must print exactly `INVALID_HEADER` to `stdout` and exit with code 1.
*   While reading records, if the file ends prematurely before a record is fully read (including its content), the program must print `TRUNCATED` to `stdout` (after printing any successfully parsed previous records) and exit with code 2.
*   For each fully read record, the program must calculate a simple Checksum modulo 256 of the `Content` bytes (sum of the byte values `uint8_t` % 256. If content length is 0, checksum is 0).
*   For each successfully parsed record, print to `stdout` on a new line exactly:
    `TS: <timestamp> | ID: <doc_id> | CHK: <checksum> | TXT: <content>`

Make sure your C++ program is robust against malformed input, as it will be tested extensively against an automated suite.