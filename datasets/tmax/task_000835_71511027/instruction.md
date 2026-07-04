You are a data analyst tasked with building a robust string processing and gap-filling pipeline for legacy sensor logs. 

We recently received a snapshot of the processing rules in an image file because the original wiki was corrupted. 
1. Use OCR (e.g., `tesseract`) to read the image located at `/app/config_rules.png`.
2. This image contains two critical pieces of information:
   a) The exact Regular Expression (Regex) required to parse the raw sensor log lines.
   b) The exact gap-filling and resampling rules needed to reconstruct missing data points.
3. Write a Python script at `/home/user/process_line.py` that reads a SINGLE raw log line from standard input (`sys.stdin.read().strip()`).
4. Your script must apply the regex found in the image. 
   - If the line DOES NOT match the regex perfectly, your script must print exactly `INVALID_FORMAT` to standard output and exit with code 0.
   - If the line DOES match, extract the start timestamp, end timestamp, value, and status.
5. Apply the gap-filling rule extracted from the image: you must generate a new string for *every second* between the start timestamp and end timestamp (inclusive). 
6. Output the gap-filled records to standard output, each on a new line, following the exact formatting rule specified in the image.
7. To demonstrate pipeline orchestration, write a bash script at `/home/user/run_pipeline.sh` that takes a filename as an argument, reads it line by line, passes each line to your Python script, and appends the output to `/home/user/pipeline.log`. (This bash script will not be heavily tested, but is required for your pipeline DAG simulation).

Ensure `/home/user/process_line.py` is robust, as it will be subjected to an automated fuzzing test with thousands of generated strings to verify bit-exact equivalence with our internal oracle.