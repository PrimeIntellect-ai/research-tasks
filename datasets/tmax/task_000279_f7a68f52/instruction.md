As a data analyst, I need your help processing stream data from a video file and building a robust data transformation script. 

We have a video file located at `/app/stream.mp4`. I need to analyze the packet sizes of different streams (video, audio, etc.) within this file.

Here is what you need to do:

1. **Write a Data Processing Script:**
   Create a Python script at `/home/user/reshape_stats.py`. This script must read a wide-format CSV from `stdin` and print a JSON array to `stdout`.
   
   The input CSV will have the following header:
   `timestamp,video_pkt_size,audio_pkt_size,subtitle_pkt_size,data_pkt_size`
   
   The rows will contain integer values representing packet sizes in bytes. Some fields might be empty (representing no packet for that stream at that timestamp).
   
   Your script must:
   - Read the wide-format CSV.
   - Reshape it into a long format internally (e.g., `timestamp`, `stream_type`, `pkt_size`).
   - Drop any rows where the `pkt_size` is empty or zero.
   - Calculate the `maximum` and `average` (mean) packet size for each `stream_type`.
   - Format the average to exactly 2 decimal places (as a string).
   - Output a JSON array of objects, sorted alphabetically by `stream_type`.
   
   Expected JSON output format example:
   ```json
   [
     {"stream_type": "audio", "max": 1024, "avg": "512.00"},
     {"stream_type": "data", "max": 50, "avg": "25.50"},
     {"stream_type": "video", "max": 45000, "avg": "21050.33"}
   ]
   ```

2. **Extract and Process Real Data:**
   Use `ffprobe` (which is pre-installed) to extract the `pts_time` (as timestamp), and the `size` of packets for the video and audio streams from `/app/stream.mp4`. 
   Format this extracted data into the wide CSV format expected by your script (you can write a quick bash or python wrapper for this step).
   Pass this CSV data into your `/home/user/reshape_stats.py` script and save the final JSON output to `/home/user/stream_summary.json`.

Ensure your `/home/user/reshape_stats.py` script is robust, as it will be rigorously tested against thousands of randomized wide-format CSV inputs to ensure the calculations and reshaping logic are mathematically flawless.