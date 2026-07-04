You are an automation specialist building a data processing pipeline for a set of IoT sensors. 

We have received a batch of sensor logs in multiple formats (CSV, JSON, and XML) located in the directory `/home/user/data/`. 
Additionally, there is an image at `/app/metrics_chart.png` that contains a global scaling factor text, formatted as "Scaling Factor: X.XX".

Your task is to write a purely Bash-based workflow (using standard tools like `awk`, `jq`, `sed`, `grep`, `sort`, `md5sum`, etc., but NO Python/Perl/Ruby) to process these logs and generate a final report.

Perform the following steps:
1. **OCR Extraction**: Use `tesseract` to read the image at `/app/metrics_chart.png` and extract the numeric scaling factor.
2. **Data Extraction & Normalization**: Read all files in `/home/user/data/`. They contain sensor readings with a timestamp, sensor ID, and temperature.
   - CSV format: `timestamp,sensor_id,temperature` (with header)
   - JSON format: `{"timestamp": <int>, "sensor": "<str>", "temp": <float>}` (one JSON object per line)
   - XML format: `<log><ts>...</ts><id>...</id><val>...</val></log>` (one per line)
   Normalize all extracted data into a common tabular format.
3. **Hash-based Deduplication**: Compute the MD5 hash of the concatenated string `timestamp+sensor_id+temperature` for each record. Remove any duplicate records that have identical hashes. Keep the first occurrence.
4. **Rolling Statistics**: Sort the deduplicated records chronologically by timestamp. For each unique `sensor_id`, compute a 3-period rolling average of the temperature. (For the first and second readings of a sensor, the rolling average is just the average of the 1 or 2 available readings).
5. **Scaling**: Multiply each rolling average by the scaling factor extracted from the image.
6. **Output**: Write the final results to `/home/user/output.csv` with the exact header `timestamp,sensor_id,scaled_rolling_avg` and values rounded to 2 decimal places.

Ensure your pipeline is robust and can be executed via a single bash script if needed, though you can run the commands interactively.