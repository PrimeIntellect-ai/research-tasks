You are a data scientist working with a batch of messy IoT sensor data. Your task is to write a Rust application that acts as a data cleaning pipeline. The pipeline must read raw sensor data, normalize it, enforce validation rules, log any rejected rows, and generate a summary report based on a text template.

The raw data is located at `/home/user/raw_sensors.csv`. It has the following columns:
`sensor_id`, `recorded_at`, `value`, `unit`

Here are the requirements for your Rust data cleaning pipeline:

1. **Normalization & Standardization:**
   - Parse the `recorded_at` timestamps. They come in two mixed formats: ISO-8601 (e.g., `2023-10-01T10:00:00Z`) and `MM/DD/YYYY HH:MM` (e.g., `10/01/2023 11:30`). Standardize all output timestamps to strict ISO-8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`. Assume the `MM/DD/YYYY HH:MM` format is implicitly UTC.
   - Convert all temperature `value`s to Celsius. If the `unit` is `F`, convert it to Celsius (C = (F - 32) * 5/9). If the unit is `C`, leave it as is. Round the final Celsius value to exactly two decimal places.

2. **Validation Checkpoints & Logging:**
   - Write any dropped rows to a log file located at `/home/user/cleaning_pipeline.log`.
   - The log file format must strictly be: `[REJECTED] Row <N>: <REASON>` where `<N>` is the 1-based index of the data row (i.e., the first row after the CSV header is 1).
   - Validation Rules (apply in this order, logging the first failure reason):
     - **TIME_PARSE_ERROR**: Reject if `recorded_at` cannot be parsed according to the two supported formats.
     - **PARSE_ERROR**: Reject if `value` cannot be parsed as an `f64` (e.g., "ERR", "N/A", or missing).
     - **OUT_OF_BOUNDS**: Reject if the final converted Celsius temperature is strictly less than -50.00 or strictly greater than 50.00.

3. **Output Generation:**
   - Write the successfully validated and normalized records to `/home/user/clean_sensors.csv`. The output CSV must have the exact headers: `sensor_id,recorded_at,value_celsius`.
   - The `value_celsius` must be formatted to two decimal places.

4. **Template-Based Text Generation:**
   - A report template exists at `/home/user/report_template.txt`.
   - Read this template, and replace the following exact placeholders with your pipeline's computed statistics:
     - `{{TOTAL_PROCESSED}}` -> The total number of data rows evaluated (excluding header).
     - `{{TOTAL_VALID}}` -> The number of rows successfully written to the clean CSV.
     - `{{TOTAL_REJECTED}}` -> The number of dropped rows.
     - `{{AVG_TEMP_C}}` -> The average of the valid, normalized Celsius temperatures, formatted to two decimal places.
   - Write the final evaluated text to `/home/user/report.md`.

You must implement this pipeline in Rust. You can create a new Cargo project in `/home/user/pipeline` to manage your code and dependencies (such as `csv` or `chrono`). Compile and execute your pipeline so that all expected output files are generated in `/home/user/`.