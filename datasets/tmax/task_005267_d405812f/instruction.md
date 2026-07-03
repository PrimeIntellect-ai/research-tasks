You are a developer organizing a messy project archive that contains both textual logs and a video recording of a system run. 

You have been provided with two main files:
1. A compressed archive of application logs at `/app/messy_logs.tar.gz`.
2. A video recording of the system dashboard during the run at `/app/system_run.mp4`.

Your task is to write and execute a Python script that processes this data concurrently and produces a consolidated, compressed summary.

Here are the specific requirements:

**1. Video Processing:**
Use `ffmpeg` to extract frames from `/app/system_run.mp4` at exactly 1 frame per second. Save them as JPEG images in `/home/user/frames/` with filenames like `frame_00.jpg`, `frame_01.jpg`, etc. The video corresponds exactly to a 60-second window starting at `2024-01-01 12:00:00` (which is second 0, i.e., `frame_00.jpg`).

**2. Log Processing:**
Extract `/app/messy_logs.tar.gz` to `/home/user/logs/`. Inside, you will find hundreds of messy text files. 
You must scan through all these files and find lines matching the exact format: 
`[SYSTEM EVENT] T=<YYYY-MM-DD HH:MM:SS> | CODE=<ALPHANUMERIC>`
*(Note: There is lots of garbage text and malformed lines you must ignore).*

**3. Correlation and Concurrent Output:**
Write a Python script that processes these log files concurrently (e.g., using `multiprocessing` or `concurrent.futures`). 
For every valid event found in the logs, determine which video second it corresponds to based on the timestamp. Then, get the file size (in bytes) of the corresponding extracted JPEG frame.

Your Python script must safely append these records concurrently to a single file `/home/user/final_events.csv`. Because multiple workers will be writing to this file simultaneously, you **must** use file locking (e.g., via `fcntl` in Python) to prevent race conditions and interleaved lines.

The CSV format should strictly be:
`Timestamp,Code,FrameSize`
*(e.g., `2024-01-01 12:00:05,A1B2,45032`)*

**4. Final Archiving:**
Once the CSV is fully written, compress it into a gzip stream and save it as `/home/user/final_events.csv.gz`.

Ensure your final script handles the file I/O safely and efficiently. The automated test will extract your final `.gz` file and score the accuracy of the extracted rows against the ground truth.