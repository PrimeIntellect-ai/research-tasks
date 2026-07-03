You are a data analyst dealing with some raw IoT sensor data. We have a CSV file located at `/home/user/readings.csv` containing historical sensor data. Unfortunately, the data collection system had a bug that caused it to sometimes write duplicate records with the same timestamp, or append "stale" rows out of order.

Your task is to build a reliable querying tool to extract the true latest reading for any given sensor, outputting it in a strict JSON document format.

Here is what you need to do:
1. Initialize an SQLite database at `/home/user/sensors.db`.
2. Import the data from `/home/user/readings.csv` into a table named `readings`. The CSV has a header row with the following columns: `sensor_id`, `timestamp`, `temperature`, `humidity`.
3. Write a bash script at `/home/user/get_latest.sh` that takes exactly one argument: the `sensor_id`.
4. Inside the script, construct a parameterized SQLite query to find the *latest* (maximum `timestamp`) reading for the provided `sensor_id`. 
5. **Handling corrupted/stale rows:** If there are multiple rows for the same sensor with the exact same maximum `timestamp`, resolve the tie by selecting the row with the highest `temperature`.
6. The script must output *only* a valid JSON object to standard output representing this reading, matching this exact schema:

```json
{
  "id": "<sensor_id>",
  "latest_reading": {
    "time": "<timestamp>",
    "temp": <temperature_as_number>,
    "hum": <humidity_as_number>
  }
}
```

Requirements:
- Ensure `/home/user/get_latest.sh` is executable.
- The script should safely pass the argument to SQLite (do not just concatenate strings if it can be avoided, though simple bash variables passed to the sqlite3 CLI are acceptable if properly quoted).
- Do not output any additional text, prompts, or SQLite headers—only the raw JSON.