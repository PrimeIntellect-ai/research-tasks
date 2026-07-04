You are acting as a systems and localization engineer. We have an automated UI translation testing pipeline that produces a video recording of a device screen and a JSON-Lines log file of the localization strings being tested. However, our logging system is currently producing malformed output, and we need a reliable data pipeline to clean the logs, synchronize them with the video, and extract visual features.

Your objective is to build an automated data processing pipeline. 

Here are the requirements:
1. **Log Parsing & Cleaning:** You are provided a malformed log file at `/app/broken_loc.jsonl`. Each line is supposed to be a JSON object with keys `frame_id` (integer), `lang` (string), and `raw_text` (string). However, the parser responsible for generating this file broke the unicode escape sequences (e.g., outputting doubly escaped strings like `\\\\u00e9` instead of `\\u00e9`, or raw literal `\x` sequences incorrectly). Write a Python script that robustly parses this file, extracts the structured information, and reconstructs the proper UTF-8 strings for `raw_text`.
2. **Video Feature Extraction:** You are provided a video artifact at `/app/video.mp4`. For each valid `frame_id` found in the log file, extract the video frame exactly at `t = frame_id` seconds. Compute the global average Red, Green, and Blue (RGB) channel pixel values for that specific frame (0-255 scale).
3. **Sorting and Integration:** Join the repaired text and the extracted visual features. Sort the final dataset in ascending order of `frame_id`.
4. **Pipeline Scheduling:** Create a master shell script at `/home/user/run_pipeline.sh` that executes your Python extraction code. Then, configure a local user `cron` job that schedules `/home/user/run_pipeline.sh` to run at the top of every minute.
5. **Output Format:** Your pipeline must write its final results to `/home/user/final_features.csv` with the exact header: `frame_id,lang,repaired_text,r_avg,g_avg,b_avg`.

Your solution will be evaluated based on the accuracy of your unicode repairs and the precision of your extracted RGB features.