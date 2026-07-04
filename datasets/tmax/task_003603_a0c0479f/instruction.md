You are a Data Analyst working on an experiment tracking pipeline. We have a broken data pipeline script and a video artefact from our latest experiment. 

Your task is to fix the pipeline, extract metadata from the video, and expose the cleaned dataset via a local API for downstream model tokenization.

Here are the requirements:
1. We have an experiment recording at `/app/experiment.mp4`. Use a Python library (like `cv2` or `imageio`) or `ffmpeg` to determine the exact total number of frames in this video.
2. We have a raw dataset at `/app/data.csv` and a processing script at `/app/pipeline.py`. 
   - The script currently reads the CSV and creates a `token` column by concatenating the string "EVT_" with the `event_code` column. 
   - However, because some `event_code` values are missing (NaN), pandas silently converts the entire column to floats. This results in tokens like `"EVT_500.0"` instead of `"EVT_500"`.
   - Fix `/app/pipeline.py` so that valid integers remain integers in the string representation (e.g., `"EVT_500"`). For rows with missing `event_code`, the token should be `"EVT_UNK"`.
3. Update the script to add a new column named `video_frames` to the DataFrame, filling every row with the total frame count you extracted from `/app/experiment.mp4`.
4. Instead of saving the dataset to disk, modify the script (or create a new one) to serve the processed DataFrame as a JSON records array over HTTP. 
   - You must start a web server (e.g., using `FastAPI`, `Flask`, or `http.server`) listening on `127.0.0.1:8000`.
   - The processed data must be returned as a JSON array of objects when a `GET` request is made to the endpoint `/api/records`. 
   - Leave this server running in the background or foreground so we can verify the output.

Ensure your API returns the exact structure expected. For example:
`[{"id": 1, "event_code": 500, "token": "EVT_500", "video_frames": 150}, ...]`