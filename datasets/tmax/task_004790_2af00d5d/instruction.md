You are an automation specialist for a climate monitoring network. We are building an ingestion pipeline for raw time-series sensor data (CSV format). Unfortunately, some sensors are experiencing firmware glitches, resulting in corrupted records. Specifically, we are seeing embedded newlines within the "sensor_notes" column that break our downstream CSV parsers, as well as malformed timestamps and unregistered sensor IDs.

Your task is to build a robust multi-stage data sanitization workflow.

Step 1: Extract Configuration
We have a scanned image of the legacy sensor schema configuration located at `/app/config/sensor_specs.png`. Use OCR tools (e.g., `tesseract`, which is preinstalled) to read this image. You must extract the exact Regular Expression used to validate a "Sensor ID". 

Step 2: Build the Python Sanitizer
Create a Python script at `/home/user/sanitizer.py`. The script must act as a CLI tool with the following signature:
`python3 /home/user/sanitizer.py <input_csv> <output_csv>`

This script must read the input CSV and write a sanitized version to the output CSV. A row must be completely dropped (omitted from the output) if it meets ANY of the following "evil" criteria:
1. It contains embedded newlines anywhere in the row (especially inside quoted strings in the `sensor_notes` column).
2. The `timestamp` column does not strictly adhere to ISO 8601 format (e.g., `YYYY-MM-DDTHH:MM:SSZ`).
3. The `sensor_id` column does not perfectly match the Regex pattern you extracted from the image in Step 1.

All valid, clean rows must be preserved exactly as they are.

Step 3: Orchestration and Templated Reporting
Write a bash script at `/home/user/pipeline.sh` that uses bash built-ins and coreutils to process a directory of CSVs. 
The script should take an input directory and an output directory:
`bash /home/user/pipeline.sh /path/to/input /path/to/output`

For every `.csv` file in the input directory, it should invoke your Python sanitizer. 
After processing, the bash script must generate a summary report at `/path/to/output/report.html` using a template-based text generation approach (you can write a simple HTML template directly in the bash script using heredocs). The HTML report must contain the exact string "Sanitization Complete", list the number of files processed, and include a validation checkpoint confirming that the output directory contains the same number of CSV files as the input.

To test your sanitizer, we have provided sample data:
- `/app/corpora/clean/` contains pristine time-series CSVs.
- `/app/corpora/evil/` contains corrupted CSVs with embedded newlines, bad timestamps, and malicious sensor IDs.
Ensure your pipeline drops the bad rows while perfectly preserving the clean ones. Our automated verifier will strictly test `/home/user/sanitizer.py` against a hidden validation set of these two corpora.