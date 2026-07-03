You are assisting a storage administrator who is managing disk space for a large-scale video archiving system. We need a custom utility to dynamically calculate the exact storage footprint of specific video segments before they are chunked and moved to cold storage tiers. 

We have a sample video file located at `/app/archive_sample.mp4`. 

Your task is to write a standalone executable script at `/home/user/segment_sizer` (ensure it has executable permissions and a proper shebang, e.g., `#!/usr/bin/env python3` or similar).

This program must do the following:
1. Read a JSON array from standard input (`stdin`). The JSON array will contain objects with `start_frame` and `end_frame` integer keys. Example: `[{"start_frame": 0, "end_frame": 15}, {"start_frame": 100, "end_frame": 105}]`.
2. For each object in the JSON array, extract the exact corresponding frames from `/app/archive_sample.mp4`. You may use `ffmpeg` or any suitable library to stream or memory-map the frame extraction. 
3. Calculate the total size in bytes of the raw, uncompressed RGB24 pixel data for the frames in the inclusive range `[start_frame, end_frame]`. 
4. Output a strict CSV format to standard output (`stdout`), with the header `start,end,bytes`. Print one row per JSON object in the exact order they were received.

Example input:
`[{"start_frame": 0, "end_frame": 2}]`

Example output:
```csv
start,end,bytes
0,2,4147200
```
*(Note: 4147200 is just an example byte size for 3 frames depending on resolution)*

The script must handle large JSON streams efficiently and exit with code 0.