You are an automation specialist tasked with building an ETL workflow to recover and process noisy telemetry data from a video feed.

We have a video file located at `/app/instrument_feed.mp4`. The raw telemetry logs are embedded in the video as a SubRip (SRT) subtitle track. 

Your objective is to create an automated pipeline that extracts this text, mathematically processes it, and loads the final pristine data into a database.

Step 1: Write a data processing filter script at `/home/user/process_feed.py`.
This script must read raw text from `stdin` and output to `stdout`. 
Requirements for `process_feed.py`:
- Scan the input text for lines containing instrument readings. Use a regex to extract the timestamp and value. The target format is exactly: `[TIMESTAMP] METRIC_VAL: VALUE` where TIMESTAMP is an integer and VALUE is a floating-point number.
- Ignore all other text, noise, or malformed lines.
- Once the valid readings are extracted, perform resampling and gap-filling. You must output a continuous time-series starting from the lowest extracted timestamp to the highest extracted timestamp, at a step of 1.
- For any missing timestamp in that range, use linear interpolation based on the nearest surrounding valid timestamps to calculate the missing value.
- Output the resulting data as a CSV to `stdout` with the header `timestamp,value` followed by the rows (values rounded to 2 decimal places).

Step 2: Orchestrate the multi-stage pipeline.
Write a bash script at `/home/user/run_pipeline.sh` that:
- Uses `ffmpeg` to extract the SRT subtitle track from `/app/instrument_feed.mp4`.
- Pipes the extracted text directly into your `/home/user/process_feed.py` script.
- Bulk imports the resulting CSV data into a SQLite database at `/home/user/telemetry.db`, into a table named `readings`.

Ensure your python script correctly handles arbitrary input (it will be heavily tested against random fuzz inputs for bit-exact equivalence with an oracle).