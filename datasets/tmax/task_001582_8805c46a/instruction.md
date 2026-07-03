You are a data scientist tasked with cleaning and aligning two datasets from different sensors that recorded data simultaneously but in completely different formats and with slightly mismatched clocks.

You need to write a Bash script located at `/home/user/clean_data.sh` that processes these files and outputs a synchronized, transformed dataset. 

**Inputs:**
1. **`/home/user/sensor_A.log`**: A text log file containing position readings.
   Format: `[YYYY-MM-DD HH:MM:SS UTC] POS: lat=<latitude>, lon=<longitude>`
   Example: `[2023-10-01 10:00:00 UTC] POS: lat=10.5, lon=-5.2`

2. **`/home/user/sensor_B.csv`**: A CSV file containing temperature readings with Unix epoch timestamps.
   Format: `epoch,temp`
   Example: `1696154402,22.5`

**Your Script's Requirements:**
1. Read and parse both files.
2. For every log entry in `sensor_A.log`:
   - Parse the timestamp and convert it to a Unix epoch.
   - Calculate the Euclidean distance of the position from the origin point `(0, 0)` using the formula: `distance = sqrt(lat^2 + lon^2)`. Round the distance to exactly 2 decimal places (e.g., `11.72`).
   - Find the single temperature reading in `sensor_B.csv` that has the **closest** epoch timestamp to the log entry's epoch. (If there's a tie, pick the one that appears first in the CSV).
3. Output the aligned data to a new file: `/home/user/aligned_data.tsv`.
   - The output must be a Tab-Separated Values (TSV) file.
   - Do not include a header row.
   - The columns must strictly be: `log_epoch` <tab> `csv_epoch` <tab> `distance` <tab> `temp`

**Constraints:**
- Your script must be written primarily in Bash and executable (`chmod +x /home/user/clean_data.sh`). You may use standard Unix utilities (like `awk`, `sed`, `grep`, `date`, `bc`, `sort`).
- Run your script to generate `/home/user/aligned_data.tsv` before finishing the task.