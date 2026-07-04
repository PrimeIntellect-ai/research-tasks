I am a researcher organizing a multi-modal dataset from a recent robotics experiment. The dataset contains a video feed and a set of compressed, multi-encoded log files organized in a messy directory structure that contains symlink loops.

I need you to build a C++ HTTP service that safely processes this dataset, correlates the logs, extracts video frames, and serves the results. 

Here are the requirements:

1. **Video Processing**:
   - There is a video file located at `/app/experiment.mp4`.
   - Use `ffmpeg` to extract all frames as JPEG images into `/home/user/frames/`.

2. **Log Processing**:
   - The logs are located in `/app/dataset/logs/`.
   - **Warning**: This directory contains symlinks that loop back on themselves (e.g., `archive/` points back to `logs/`). Your C++ code must safely traverse the directory without entering infinite loops.
   - You will find `.gz` files. Read these compressed streams directly in your C++ application (you can use `zlib` or similar libraries; feel free to install any necessary dev packages via `apt`).
   - `sensor_a.log.gz` is encoded in UTF-8.
   - `sensor_b.log.gz` is encoded in UTF-16LE. You must convert it to UTF-8 in memory.
   - Both logs contain multi-line records. Each record begins with the exact string `[EVENT]` on its own line, followed by several lines of data, and ends when the next `[EVENT]` appears or the file ends. Count the total number of `[EVENT]` records across all unique files.

3. **Frame Serving Directory**:
   - Create a directory `/home/user/serve/`. 
   - Write a script or C++ routine to safely populate this directory with hardlinks to the JPEGs in `/home/user/frames/`. To ensure no partial files are ever served if we update them later, perform this link creation atomically (e.g., create a hardlink in a temporary directory, then atomically move/rename the directory into place, or symlink the directory itself).

4. **HTTP API Server**:
   - Write a C++ HTTP server (you may install and use `cpp-httplib`, `crow`, or any similar library) listening on `127.0.0.1:9090`.
   - Implement the following endpoints:
     - `GET /api/stats` -> Returns a JSON response exactly like this: `{"total_frames": X, "total_events": Y}` where X is the number of extracted frames and Y is the total number of parsed multi-line events.
     - `GET /api/frames/:id` -> Returns the JPEG image for frame `:id` (e.g., `1.jpg`) from your atomic serve directory.

Please install all necessary dependencies, write the C++ code, compile it, and leave the server running in the background.