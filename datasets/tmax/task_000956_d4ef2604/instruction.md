You are an automation specialist creating a time-series processing workflow for high-frequency IoT sensor data. 

Your task consists of two parts: fixing a vendored dependency and writing a stream-processing bash script.

### Part 1: Fix and Install the Vendored Package
We use `datamash` for fast command-line aggregations, but the provided source package is broken.
1. The GNU datamash 1.8 source is located at `/app/vendored/datamash-1.8`.
2. A previous developer accidentally broke the `configure` script by inserting an `exit 1` on line 15.
3. Fix the `configure` script, build the package, and install it locally using `./configure --prefix=/home/user/local && make && make install`.
4. Ensure your script can use the installed `datamash` executable (e.g., add `/home/user/local/bin` to your PATH).

### Part 2: Time Series Processing Script
Write a bash script at `/home/user/process_sensor_data.sh` that reads a wide-format CSV stream from standard input (no headers) and outputs a long-format, downsampled CSV.

**Input format:**
Each line contains a Unix timestamp in milliseconds, followed by three sensor readings (floating-point numbers).
Example:
`1672531205123,10.5,12.1,9.8`
`1672531215456,11.0,11.9,10.0`

**Processing Requirements:**
1. **Wide-to-Long Reshaping:** Convert the row into three separate records for each sensor. The sensors are indexed 1, 2, and 3 respectively.
2. **Time-based Bucketing:** Downsample the timestamps into 1-minute (60000 ms) buckets. The bucket timestamp is the *floor* of the timestamp to the nearest minute boundary (i.e., `(timestamp_ms / 60000) * 60000`).
3. **Aggregation:** Group the data by the bucketed timestamp and the sensor index. Calculate the mean value for each group.
4. **Output Format:** Comma-separated format: `bucket_timestamp_ms,sensor_index,mean_value`. 
   - Round the mean value to exactly 2 decimal places (e.g., `10.75`).
   - The output must be sorted numerically by timestamp (ascending), and then by sensor index (ascending).

Your script must handle large input files efficiently by streaming the data and utilizing basic shell tools (`awk`, `sed`, `sort`, and `datamash`). 

Ensure your script is executable (`chmod +x /home/user/process_sensor_data.sh`). Your script will be tested against randomly generated inputs to verify bit-exact output equality with an oracle.