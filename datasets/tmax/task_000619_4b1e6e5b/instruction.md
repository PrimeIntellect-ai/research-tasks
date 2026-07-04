You are an automation specialist tasked with building a robust data processing pipeline for log sanitization.

Your objective is to create a Rust-based log sanitizer and a cron schedule for an automated ETL workflow. 

1. **Configuration Extraction**:
You have been provided with an image file containing the current pipeline constraints at `/app/settings.png`. You must use a tool like `tesseract` to read the configuration values from this image. The image contains three lines specifying `BLOCK_ID`, `MAX_ROLLING_SUM`, and `WINDOW`.

2. **Rust Sanitizer Development**:
Create a Rust project in `/home/user/sanitizer_project` and compile a release binary to `/home/user/sanitizer`. 
The binary must accept exactly two arguments: an input file path and an output file path.
`./sanitizer <input.json> <output.json>`

The input will be a JSON file containing an array of log records. Each record is an object with three fields: `id` (integer), `val` (integer), and `tag` (string). 

Your sanitizer must process the array in order and write a sanitized JSON array to the output file according to these rules:
- **Rule A**: Drop any record where the `tag` matches the `BLOCK_ID` extracted from the image.
- **Rule B**: Maintain a rolling window of the most recent *accepted* `val` integers. The size of this window is defined by `WINDOW` from the image. If adding the current record's `val` to the sum of the (up to `WINDOW - 1`) previous *accepted* values causes the total to exceed `MAX_ROLLING_SUM`, the current record must be dropped. 
- Dropped records do not enter the rolling window.

3. **Pipeline Scheduling**:
Create a crontab file at `/home/user/pipeline.cron` that schedules a hypothetical script `/home/user/run_pipeline.sh` to run every 15 minutes, but only on weekdays (Monday through Friday).

Ensure your Rust tool is robust and accurately enforces the rolling aggregation constraints. Test it thoroughly, as it will be evaluated against a hidden corpus of clean and malicious log files.