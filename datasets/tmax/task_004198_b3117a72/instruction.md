You are a data analyst tasked with cleaning up a corrupted detection dataset and serving the aggregated results. A previous pandas pipeline introduced a bug where missing values caused integer IDs to be converted to floats (e.g., `12.0` instead of `12`), and some rows have `NaN` or empty strings for `frame_id` or `object_id`.

Your objectives:
1. **Data Cleaning**: Write a Bash script to process `/app/detections.csv`. 
   - Remove any rows where `frame_id` or `object_id` is `NaN`, `NA`, or empty.
   - Convert all `frame_id` and `object_id` values from floats to integers (e.g., `12.0` becomes `12`).
   - Calculate a new column `area` which is `w * h`.
   - Save the cleaned data to `/home/user/cleaned_detections.csv` (comma-separated, with header `frame_id,object_id,x,y,w,h,area`).
2. **Video Feature Tracking**: We have a video at `/app/traffic.mp4`. Extract frames at 1 frame per second. For experiment tracking, count the total number of frames extracted and append `Total Frames: <count>` to `/home/user/experiments.log`.
3. **API Service**: Write a lightweight server (you may use Python or bash+socat) that listens on `0.0.0.0:8080`.
   - **GET `/area?object_id=<ID>`**: Must return a plain text response with the sum of the `area` for the requested integer `object_id` from the cleaned dataset.
   - **GET `/secure_stats`**: Must enforce a Bearer token. If the request header `Authorization: Bearer ds_token_2024` is present, return `200 OK` with body `{"status": "ok"}`. Otherwise, return `401 Unauthorized`.

Ensure the server is running in the background before you finish. The primary data transformations must be executed using Bash/Unix command-line tools (e.g., `awk`, `sed`), though the server can be written in Python.