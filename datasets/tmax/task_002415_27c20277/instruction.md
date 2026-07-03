You are an AI assistant acting as a data scientist. We have recorded a raw experiment video located at `/app/experiment.mp4`. You need to build a data extraction and cleaning pipeline, then serve the cleaned mathematical data via an HTTP API.

Follow these exact steps:

1. **Extract Data (Mathematical Signal):**
   Analyze the video `/app/experiment.mp4`. For each frame, calculate the average grayscale intensity (mean pixel value, 0-255). Save this raw time-series data to `/home/user/raw_signal.csv` with columns `frame_index` (starting at 0) and `intensity`.

2. **Clean the Dataset:**
   Write a script to clean the `raw_signal.csv` data.
   - First, calculate the global mean and global sample standard deviation of the `intensity` column.
   - Remove any outliers (frames where the intensity is strictly greater than 3 standard deviations away from the global mean).
   - Next, apply a 5-frame right-aligned moving average to the remaining data (i.e., the smoothed value at index `i` is the average of the intensities at `i, i-1, i-2, i-3, i-4`. For the first 4 points, just average the available points up to that index).
   - Save the final cleaned data to `/home/user/cleaned_signal.json` as a list of objects: `[{"frame_index": 0, "smoothed_intensity": 105.2}, ...]`. 

3. **Pipeline Automation & Logging:**
   Create a bash script `/home/user/pipeline.sh` that runs the extraction and cleaning steps. The script must log its progress to `/home/user/pipeline.log`. 
   The log must contain the lines:
   `[INFO] Starting extraction`
   `[INFO] Extraction complete`
   `[INFO] Starting cleaning`
   `[INFO] Cleaning complete`

   Run your pipeline script so the output files are generated.

4. **Serve the Data (Multi-Protocol):**
   Create and start an HTTP server listening on `127.0.0.1:8080`.
   The server must require an Authorization header: `Authorization: Bearer ds-secret-token` for all endpoints. If missing or invalid, return a 401 Unauthorized status.
   
   The server must expose two endpoints:
   - `GET /api/data` : Returns the contents of `/home/user/cleaned_signal.json` with a 200 OK status and `application/json` content type.
   - `GET /api/status` : Returns a JSON object `{"latest_log": "<exact text of the last line in /home/user/pipeline.log>"}`.

Leave the HTTP server running in the background.