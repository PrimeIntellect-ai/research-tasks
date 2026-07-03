You are an automation specialist tasked with creating a data processing workflow to handle incoming IoT sensor metrics.

Raw sensor data is dropped into the directory `/home/user/incoming/` as `.dat` files. You need to write a Bash-based workflow (e.g., a script or terminal commands) that processes this data and produces a finalized summary file. 

The workflow must perform the following operations:

1. **Hash-Based Deduplication**: 
   Occasionally, the system receives exact duplicate files due to network retries. Find any files in `/home/user/incoming/` that have identical MD5 hashes. Keep the file that comes first alphabetically by filename, and delete the duplicates from the directory.

2. **Data Parsing & Filtering**:
   The remaining unique `.dat` files contain comma-separated values in the format:
   `Timestamp(UnixEpoch),DeviceID,MetricValue`
   Filter the data to only include records for the device `DEV01`.

3. **Feature Extraction & Resampling**:
   We need to bin the readings for `DEV01` into 1-hour (3600-second) intervals. The tracking period starts exactly at epoch `1672531200` (Interval 0) and lasts for 5 total intervals (Intervals 0, 1, 2, 3, and 4). 
   For each interval, calculate the *maximum* `MetricValue` received during that hour. 

4. **Gap-Filling**:
   IoT sensors sometimes drop offline. If an interval has absolutely no readings for `DEV01`, you must forward-fill the maximum value from the immediate previous interval. (Assume a starting default value of `0` if Interval 0 has no readings, though in this dataset, Interval 0 will have data).

Output the final 5 intervals to `/home/user/processed_dev01.csv` in the format:
`IntervalIndex,MaxValue`

The file must have exactly 5 lines (for intervals 0 through 4) sorted by `IntervalIndex`. No headers should be included.

You may use Bash alongside standard Unix utilities (like `awk`, `sort`, `md5sum`, etc.) or write a small script (e.g., Python/Perl) triggered by Bash to handle the gap-filling logic, but Bash must be the primary driver. Execute your workflow to produce the final `processed_dev01.csv`.