You are acting as a storage administrator responding to a catastrophic backup failure. A rogue backup script created an infinite symlink loop, flooding the backup drive. Simultaneously, the system monitoring dashboard recorded a video of the incident before crashing.

You need to analyze the damage and expose your findings via a local HTTP API so the automated recovery system can query them. 

Write and start an HTTP server listening on `127.0.0.1:8080`. Your service must implement the following endpoints:

1. `GET /video-analysis`
You have been provided a system recording at `/app/disk_monitor.mp4`. 
The system crashed and the screen went completely black (rgb: 0,0,0) for several frames during the recording.
Use `ffmpeg` (which is preinstalled) or any other tool to analyze the video. Find the exact number of purely black frames.
Response Format: JSON object `{"black_frames_count": <integer>}`.

2. `GET /storage-scan`
A partial dump of the corrupted backup is located at `/home/user/storage_dump/`.
This directory contains an infinite symlink loop. You must safely traverse this directory, ignoring symlinks that point back up the tree, to find all regular files with the `.dat` extension.
For each `.dat` file found, extract its binary header (the first 4 bytes) as a lowercase hex string.
Response Format: JSON array of objects, sorted alphabetically by file path:
`[{"path": "<absolute_path_to_file>", "header": "<hex_string>"}, ...]`

3. `POST /clean-config`
The backup agent uses an XML configuration format. The crash corrupted the file with thousands of redundant `<loop_detected/>` tags.
The endpoint will receive raw XML in the request body. You must parse it, perform a large-scale text edit to remove all `<loop_detected/>` elements (and their enclosing whitespace if any), and return the cleaned XML as a raw string. 

You may use any programming language or shell tools to accomplish this. Ensure your server runs in the foreground or stays active so the verifier can test it. Keep symlink resolution efficient!