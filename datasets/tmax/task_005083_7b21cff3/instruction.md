You are a log analyst investigating patterns in a legacy monitoring system. The system's dashboard was recorded to video, and you need to build an automated pipeline to extract, validate, and aggregate the data.

Your task consists of the following steps:

1. **Video Data Extraction**:
   You have a video artifact located at `/app/data/dashboard.mp4`. Use `ffmpeg` and Python to extract the first 30 frames from this video (at its native framerate). For each of these 30 frames, calculate the average grayscale pixel intensity (0-255). 
   Save this data to `/home/user/raw_metrics.csv` with the header `frame_index,intensity`. (Frame index should start at 0).

2. **Resampling and Gap-Filling**:
   Assume the video extraction sometimes drops frames. Read `/home/user/raw_metrics.csv` and resample the data so that there is exactly one row for every integer `frame_index` from 0 to 29. If any frame index is missing, fill the `intensity` gap using linear interpolation.
   Save the result to `/home/user/filled_metrics.csv`.

3. **Data Validation (Adversarial Corpus)**:
   You must write a robust validation script `/home/user/validate.py` that takes a single CSV file path as a command-line argument. The script should verify the mathematical and structural integrity of the log file.
   - It must exit with code `0` (Clean) if the file:
     - Has exactly two columns with headers `frame_index,intensity`.
     - `frame_index` consists of strictly increasing, contiguous integers starting from 0.
     - `intensity` consists of valid floating-point numbers strictly between 0.0 and 255.0 (inclusive).
   - It must exit with code `1` (Evil) if the file violates ANY of these rules (e.g., non-numeric data, missing rows, negative intensities, or values > 255).
   
   Two corpora are provided to test your script:
   - `/app/corpus/clean/`: Contains valid CSVs.
   - `/app/corpus/evil/`: Contains malformed or mathematically impossible CSVs.
   Your script must perfectly classify these corpora.

4. **Database Aggregation**:
   Create a bash script `/home/user/aggregate.sh` that uses SQLite3 to bulk import `/home/user/filled_metrics.csv` into a database at `/home/user/metrics.db` (table name `logs`). 
   The script must then execute a query to calculate the average intensity grouped by windows of 10 frames (i.e., frames 0-9, 10-19, 20-29). The output should be exported to `/home/user/summary.csv` with columns `window_start,avg_intensity`.

5. **Pipeline Scheduling**:
   Write a cron expression to execute `/home/user/aggregate.sh` every hour on the hour. Save just the cron string (e.g., `0 * * * * /home/user/aggregate.sh`) into a file at `/home/user/cron_schedule.txt`. Do not install the crontab, just write the file.

Ensure all paths and file formats precisely match these instructions.