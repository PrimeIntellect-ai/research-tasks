You are a log analyst investigating physical access patterns to a secure server room. We have access logs from the keycard system, event timestamps from the door sensors, and a surveillance video of the hallway. You need to build a data pipeline that correlates the logical access records with the physical video evidence.

Your objective is to write a Python script at `/home/user/analyze.py` that merges the log files, validates the data, and extracts brightness metrics from the video at the exact timestamps of the events. 

The script must accept exactly four positional arguments in this order:
`python3 /home/user/analyze.py <video_path> <users_csv> <events_csv> <output_jsonl>`

Here are the requirements for the processing pipeline:

1. **Join & Merge**: 
   - Read `<users_csv>` (columns: `event_id`, `username`) and `<events_csv>` (columns: `event_id`, `timestamp_sec`).
   - Perform an inner join on `event_id`.

2. **Data Validation**:
   - Filter the merged data to keep only rows that strictly meet both constraints:
     - `username` must consist of exactly 3 or 4 uppercase letters (e.g., `ALC`, `BOBB`).
     - `timestamp_sec` must be a valid non-negative float (e.g., `0.0`, `4.52`) and must not exceed the total duration of the video. (Assume the video `/app/surveillance.mp4` is exactly 10.0 seconds long for boundary checking, so `timestamp_sec` <= 10.0).

3. **Video Processing**:
   - For each valid event, extract the specific video frame at the given `timestamp_sec`. You may use `cv2` (OpenCV) or `ffmpeg` to seek to the timestamp. If using `cv2`, calculate the frame index as `int(timestamp_sec * fps)`.
   - Convert the extracted frame to grayscale.
   - Calculate the mean (average) pixel brightness of the grayscale frame.
   - Apply a mathematical `floor` to this mean value to get an integer (e.g., 104.89 -> 104).

4. **Output Generation**:
   - Write the results to `<output_jsonl>` as a JSON Lines file.
   - Each line must be a JSON object containing: `{"event_id": "...", "username": "...", "brightness": <int>}`.
   - The output lines MUST be sorted alphabetically by `event_id`.

The system already has Python 3, `pandas`, `opencv-python`, and `ffmpeg` installed. 
You can test your script using the provided video at `/app/surveillance.mp4`. To ensure your code is completely robust, an automated tester will run your script against multiple randomly generated pairs of CSV files and verify the output matches a reference implementation bit-for-bit.