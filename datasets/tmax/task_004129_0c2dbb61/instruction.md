I need your help organizing and parsing a complex historical sensor dataset. I am a researcher, and my data collection system generated a massive amount of logs. The data is currently stored in a nested archive, and the files are large enough that you need to be careful with memory. 

Here are the details:
1. **The Data Source:** 
   There is a main archive located at `/home/user/sensor_data/master_archive.tar`. Inside this tar file, there are several `.zip` files (e.g., `group_1.zip`, `group_2.zip`). Inside each `.zip` file, there are large text files ending in `.log`.

2. **The Data Format:**
   Each `.log` file contains millions of lines of sensor readings. The format of each line is:
   `TIMESTAMP | SENSOR_ID | VALUE | STATUS`
   Example:
   `2023-10-01T12:00:00Z | SENSOR_X | 42.5 | OK`

3. **The Problem (Noise):**
   Due to a bug in the logging system, the `VALUE` column is frequently corrupted with an inline noise tag that looks like `[ERR_NOISE_XXX]` where `XXX` is a random 3-digit number. 
   Example of corrupted line:
   `2023-10-01T12:00:01Z | SENSOR_Y | 18.2[ERR_NOISE_404] | OK`
   You must strip out these noise tags completely to recover the true numeric value (e.g., `18.2`). Lines without noise should be parsed normally. 

4. **Your Goal:**
   - Recursively traverse the nested archives (`.tar` -> `.zip` -> `.log`).
   - Use streaming or memory-mapped I/O techniques to read the files so you don't load entire large log files into memory at once.
   - Clean the data by removing the noise tags.
   - Calculate the total sum of the values and the count of readings for each unique `SENSOR_ID` across *all* log files. Only include lines where `STATUS` is `OK`. Ignore lines with `STATUS` as `WARN` or `ERROR`.
   - You can write your solution in Python, Bash, or a combination of both.

5. **The Output:**
   Create a JSON file at `/home/user/results/summary.json` containing the aggregated data. The format must be exactly:
   ```json
   {
     "SENSOR_X": {
       "sum": 105.2,
       "count": 3
     },
     "SENSOR_Y": {
       "sum": 450.0,
       "count": 15
     }
   }
   ```
   (Note: Use standard floating-point precision for the sum, and integer for the count. Round the sum to 2 decimal places before saving to JSON).

Please write and execute the necessary scripts to accomplish this. Do not ask me for permission to run commands. Ensure the `/home/user/results` directory is created if it doesn't exist.