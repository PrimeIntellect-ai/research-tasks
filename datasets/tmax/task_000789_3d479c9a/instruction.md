You are an automation specialist building a data processing workflow for an IoT sensor network. You need to write a Rust program that cleans raw sensor data, resamples it to handle irregular intervals, computes daily statistics, and generates a markdown report from a template.

**Environment details:**
- Raw data file: `/home/user/sensor_data.csv`
- Report template: `/home/user/report_template.md`
- Output report file: `/home/user/daily_report.md`

**Pipeline Requirements:**

1. **Constraint-Based Validation**:
   - Read `/home/user/sensor_data.csv`. The format is `timestamp,sensor_id,temperature` (comma-separated, no header).
   - Ignore any lines that are malformed.
   - Discard any records where the `temperature` is outside the valid range of `-20.0` to `60.0` (inclusive).

2. **Resampling and Gap-Filling**:
   - We need to generate a regular time series of temperature values for a specific 24-hour target period: starting at Unix epoch `1710000000` and ending at `1710086400` (inclusive).
   - The interval between points is exactly 1 hour (`3600` seconds). This means you must generate exactly 25 data points: `1710000000`, `1710003600`, `1710007200`, ..., `1710086400`.
   - **Forward-fill rule:** For each target timestamp `T`, the temperature value is the temperature of the *most recent valid record* whose timestamp is less than or equal to `T`. 
   - If there are no valid records with a timestamp `<= T`, use the default value `0.0`.

3. **Summary Statistics**:
   - Calculate the `min`, `max`, and `mean` (average) of the exactly 25 resampled temperature values computed in the previous step.
   - Format the `mean` to exactly two decimal places (e.g., `15.34`). Format `min` and `max` to one decimal place (e.g., `12.0`).

4. **Template-Based Generation**:
   - Read the contents of `/home/user/report_template.md`.
   - Replace the literal strings `{{MIN}}`, `{{MAX}}`, and `{{MEAN}}` with your calculated statistics.
   - Save the resulting text to `/home/user/daily_report.md`.

Write the Rust code, compile it, and run it so that the final `/home/user/daily_report.md` file is produced. You may use any standard Rust tools available in a standard installation (using `cargo` or `rustc`). Do not use any external crates; the standard library is sufficient.