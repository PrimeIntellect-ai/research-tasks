You are acting as a backup administrator investigating a critical database crash. You have recovered two key artifacts from the incident: a raw Write-Ahead Log (WAL) file and a security camera recording of the server room. You need to process these files, extract the relevant incident data, and serve the bundled archive over an API for the remote forensics team.

**Step 1: Process the Write-Ahead Log**
There is a custom-format binary WAL file located at `/app/db_system.wal`.
The file consists of sequentially packed records. Every record follows this exact binary structure:
- `Timestamp`: 8-byte big-endian unsigned integer (Unix timestamp).
- `Record Type`: 1-byte unsigned integer (`0x01`=INFO, `0x02`=WARN, `0x03`=CRITICAL).
- `Payload Length`: 4-byte big-endian unsigned integer.
- `Payload`: Raw byte array of length equal to the `Payload Length`.

Your task is to write a Python script that reads `/app/db_system.wal`, filters out all records EXCEPT the `0x03` (CRITICAL) records, and writes the filtered critical records to `/home/user/filtered.wal`.
*Requirement:* The write must be atomic. You must write the filtered binary data to a temporary file in `/home/user/` first, and then atomically replace (rename) it to `/home/user/filtered.wal` to prevent partial reads by other tools.

**Step 2: Extract Video Evidence**
There is a video file of the server room at `/app/server_room_cam.mp4`.
Using `ffmpeg` (which is pre-installed), extract exactly one frame at the start of seconds 10, 11, 12, 13, 14, and 15 of the video.
Save these frames in the directory `/home/user/frames/` with the exact naming convention `frame_10.jpg`, `frame_11.jpg`, etc.

**Step 3: Serve the Archive Data via API**
Write and start a Python HTTP server (you may use `Flask`, `FastAPI`, or the standard `http.server`) that listens on `127.0.0.1:8000`. Keep this process running in the background.

The server must expose the following routes:
1. `GET /api/wal` -> Returns the exact binary contents of `/home/user/filtered.wal` with `Content-Type: application/octet-stream`.
2. `GET /api/frame/<second>` -> (e.g., `/api/frame/12`) Returns the corresponding JPEG file from the `frames` directory with `Content-Type: image/jpeg`. If the requested second does not exist, return a 404.

*Security Requirement:* The forensics team requires basic authentication. Every request to the above endpoints MUST include an `Authorization` HTTP header with the exact value:
`Bearer archiver_token_x7z`
If this header is missing or incorrect, the server must return a `401 Unauthorized` status code.