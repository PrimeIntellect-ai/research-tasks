You are tasked with building a constraint validation script for a configuration tracking manager. 

We maintain a series of configuration snapshot logs in wide CSV format. You must create an executable script at `/home/user/validate_config.sh` that takes a single file path as an argument. The script must evaluate the CSV file against a set of business rules and exit with status code `0` if the file is valid, and exit with status code `1` if the file violates any rule.

**Input CSV Format:**
The files have the header: `timestamp,cpu_limit,mem_limit,net_limit`
The `timestamp` is a float representing seconds. The limits are integers. The rows are sorted by `timestamp` in ascending order.

**Validation Rules:**
1. **Constraint-based Validation & Reshaping:** Conceptually reshape the data from wide to long format (`timestamp, metric, value`). No individual metric value (`cpu_limit`, `mem_limit`, or `net_limit`) may strictly exceed `100`.
2. **Rolling Statistics:** The rolling 3-period simple moving average of the `cpu_limit` metric must not strictly exceed `80.00`. (For the first row, the average is just the first row's value. For the second row, it's the average of the first two rows. From the third row onwards, it is the average of the current row and the two preceding rows).
3. **Video-Linked Feature Extraction:** There is a video recording of our legacy dashboard indicator at `/app/dashboard.mp4`. The video runs at exactly 10 frames per second. Most frames are solid black. However, a "system reset" is indicated by a frame being completely solid red (RGB: 255, 0, 0). 
   Let $T$ be the set of reset timestamps derived from the video, calculated as $timestamp = frame\_index / 10.0$ (where `frame_index` is 0-indexed). 
   If a row in the CSV has a `timestamp` that exactly matches a timestamp in $T$, the `mem_limit` for that row MUST be exactly `0`.

**Testing & Verification:**
Your script will be tested against two hidden directories of CSV logs:
- Clean corpus: Valid logs that adhere to all rules.
- Evil corpus: Invalid logs, each violating at least one of the rules.

Your script must run natively on standard Linux using typical pre-installed utilities (e.g., bash, awk, jq, python3, ffmpeg). You may use any language for your script, provided it has the exact signature: `./validate_config.sh <path_to_csv>`.