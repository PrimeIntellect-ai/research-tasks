I need you to help me clean up and organize an experimental dataset. I am a researcher studying robotic movements, and I have a large collection of telemetry logs and video recordings. Unfortunately, some of our telemetry logs have been corrupted or deliberately tampered with by a rogue process, and I need a robust filter to separate the good data from the bad.

First, I have a reference video of a robotic run located at `/app/experiment_video.mp4`. I need you to analyze this video using `ffmpeg`/`ffprobe` and create a simple CSV file at `/home/user/video_frames.csv` containing two columns: `frame_index` and `pkt_size` (the size of each frame in bytes). Use a bash script or command to achieve this.

Second, I have a dataset of custom Write-Ahead Logs (WAL) located in `/dataset/`. These logs contain structured telemetry data (mixed binary and JSON). I need you to write a C program at `/home/user/wal_filter.c` that reads a WAL file, validates its structure, and decides if it is safe or malformed.
A valid WAL file in our custom format has:
1. A 4-byte magic number: `WAL\x00`
2. A 4-byte unsigned integer (little-endian) representing the length of the JSON metadata.
3. The JSON metadata string (must be valid JSON and contain a `"checksum"` field).
4. A zlib-compressed binary payload.

An "evil" WAL file might have an invalid magic number, a truncated JSON payload, invalid JSON syntax, or a zlib payload that fails to decompress or mismatches the expected size.

Your C program should take a single file path as an argument. It must output exactly the word `CLEAN` to stdout if the file is perfectly valid, or `EVIL` if it violates any of the structure rules or has corruption.

Compile your program to `/home/user/wal_filter`. Ensure it is robust against malformed inputs (e.g., buffer overflows, unexpected EOF).

Finally, process all files in the dataset using your C program and output a log file at `/home/user/dataset_classification.log` where each line is formatted as:
`[filename] [CLEAN/EVIL]`