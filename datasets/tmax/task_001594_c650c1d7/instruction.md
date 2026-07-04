You are a data engineer building a lightweight ETL pipeline step. You need to write a Go program that processes a stream of JSON lines containing sensor data, applies validation rules, extracts and transforms features, and computes rolling statistics.

An input file is located at `/home/user/input.jsonl`. Each line is a JSON object with the following schema:
`{"ts": int, "id": string, "tk": float64, "h": float64}`
Where `ts` is a timestamp, `id` is the sensor ID, `tk` is the temperature in Kelvin, and `h` is the relative humidity percentage.

Your task is to write a Go program at `/home/user/etl.go` that reads these JSON lines from standard input (stdin) and writes a CSV to standard output (stdout). 

The program must implement the following pipeline logic:
1. **Validation Gate**: Read each line and discard it entirely if it fails any of these quality checks:
   - `tk` (Temperature in Kelvin) is missing, exactly 0, or negative.
   - `h` (Humidity) is less than 0.0 or greater than 100.0.
   - `id` is empty.
2. **Feature Extraction**: For valid records, transform the `tk` (Kelvin) value into a new feature `temp_c` (Celsius). The formula is `temp_c = tk - 273.15`.
3. **Rolling Statistics**: Maintain a global rolling average of the `temp_c` values for the last 3 *valid* records processed (regardless of sensor `id`). If fewer than 3 valid records have been processed so far, compute the average using however many valid records are currently available.
4. **Output Format**: Write the results as a CSV with the header `ts,id,temp_c,rolling_avg_temp_c`. 
   - Both `temp_c` and `rolling_avg_temp_c` must be formatted to exactly 2 decimal places (e.g., using `%.2f`).

Finally, execute your Go program to process `/home/user/input.jsonl` and save the output to `/home/user/output.csv`. 

For example, your execution command will look like:
`go run /home/user/etl.go < /home/user/input.jsonl > /home/user/output.csv`