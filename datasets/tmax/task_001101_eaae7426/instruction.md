You are a data analyst tasked with processing multi-modal data from an industrial experiment. We recorded a sensor's output (CSV) and a camera feed (MP4 video) observing a light beacon. The systems were not perfectly synchronized, and the sensor samples at an irregular high frequency, while the video is 30 FPS.

Your goal is to build a data processing pipeline that extracts the video signal, buckets the sensor data, aligns the two time series by finding the optimal time shift, and prepares a scheduled job configuration.

**Inputs provided to you:**
1. `/app/experiment.mp4`: A video recording of the beacon. The brightness of the video frames fluctuates over time. The video recording started roughly around the Unix epoch timestamp `1700000000` (seconds), but the exact start time has an unknown offset.
2. `/app/sensor.csv`: A CSV file with two columns: `timestamp_ms` (Unix timestamp in milliseconds) and `luminosity_raw` (float). 

**Your tasks:**

1. **Video Processing (Signal Extraction):**
   Extract the average brightness of the video per second. You may use `ffmpeg` with filters (e.g., `signalstats` or generating 1 FPS thumbnails and calculating their average pixel values) to get a 1-second resolution brightness time series.

2. **Time-Based Bucketing (Sensor Data):**
   Parse `/app/sensor.csv` and aggregate the `luminosity_raw` into 1-second buckets (using the floor of the timestamp in seconds). Calculate the average raw sensor value for each 1-second bucket.

3. **Normalization and Alignment (Mathematical):**
   Min-max normalize both the 1-second video brightness array and the 1-second sensor array (so values range from 0.0 to 1.0). 
   The video start time is approximately `1700000000` but has an unknown integer shift in seconds (between -15 and +15 seconds). 
   You must find the optimal integer time shift (in seconds) that maximizes the Pearson correlation between the normalized video brightness and the normalized sensor luminosity.

4. **Final Output:**
   Generate an aligned CSV file at `/home/user/aligned.csv` containing the optimally synchronized data.
   Format: `timestamp_sec,normalized_brightness,normalized_sensor`
   Include only the overlapping timestamps where both a video brightness value and a sensor value exist after applying the optimal shift. Keep the CSV header exactly as written.

5. **Pipeline Scheduling:**
   We want to run a hypothetical script `/home/user/process_latest.sh` every hour at 15 minutes past the hour. Create a crontab file at `/home/user/crontab.txt` with the appropriate cron expression and command.

Use bash, awk, and Python as needed. Make sure your output is clean and perfectly formatted. Our automated verification suite will measure the Pearson correlation of the two data columns in your `aligned.csv`. You must achieve a correlation of >= 0.90.