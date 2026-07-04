You are a data scientist working with a raw IoT telemetry time-series dataset. The dataset is located at `/home/user/telemetry.csv`. 

It is a standard RFC 4180 compliant CSV file with the following header:
`timestamp,sensor_id,ip_address,payload,notes`

You need to create a data cleaning pipeline. Previous attempts using naive `awk` and `grep` pipelines failed because the `notes` column frequently contains quoted embedded newlines, which caused those scripts to silently drop or corrupt rows.

Write a Bash script at `/home/user/clean_data.sh` that reads `/home/user/telemetry.csv` and streams the processed output to `/home/user/clean_telemetry.csv`. 

Your script must perform the following transformations:
1. **Handle Embedded Newlines:** Properly parse the CSV so that rows with embedded newlines in the `notes` column are not corrupted or dropped.
2. **Feature Extraction:** The `payload` column contains a JSON string (e.g., `{"temp": 22.1, "status": "ok"}`). Extract the numerical value associated with the `temp` key. 
3. **Filtering:** If a row's JSON `payload` does not contain a `temp` key, drop the entire row from the output.
4. **Data Masking (Anonymization):** Mask the `ip_address` column by replacing the final octet of the IPv4 address with `XXX` (e.g., `192.168.1.101` becomes `192.168.1.XXX`).
5. **Output Formatting:** The output file `/home/user/clean_telemetry.csv` must be a valid CSV with exactly the following header:
   `timestamp,sensor_id,masked_ip,temperature`
   Followed by the extracted and cleaned data rows.

Ensure your script is executable (`chmod +x /home/user/clean_data.sh`). You may use any standard Linux command-line tools (e.g., `jq`, `python3`, `awk`) inside your Bash script to achieve this, as long as it handles the data as a stream (does not load the entire file into memory at once). Once you have written the script, execute it so the output file is generated.