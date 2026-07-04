You are a Machine Learning Engineer preparing sensor data for a predictive maintenance model. The raw data is delivered in a large binary format, but it contains corrupted entries and needs feature engineering and statistical filtering before it can be used for training.

Your task is to write a C program that reads the raw binary data, enforces a schema by filtering out corrupted records, engineers a new feature, performs a statistical hypothesis test (Confidence Interval) to find "drifting" sensors, and stores the results in a SQLite database.

**Step 1: Environment Setup**
You will need to install the SQLite3 development libraries to interact with SQLite from C (`libsqlite3-dev`). 

**Step 2: Input Data Schema**
The input data is located at `/home/user/raw_sensors.bin`. It contains thousands of records written sequentially. Each record strictly follows this C struct (packed, little-endian):

```c
#pragma pack(push, 1)
struct SensorRecord {
    uint32_t sensor_id;
    uint64_t timestamp;
    float value;
    uint32_t checksum;
};
#pragma pack(pop)
```

**Step 3: Schema Enforcement (Data Cleaning)**
Read the records from the binary file. You must discard any record that is corrupted. A record is valid IF AND ONLY IF its `checksum` equals `sensor_id ^ (timestamp & 0xFFFFFFFF)`. Ignore invalid records completely.

**Step 4: Feature Engineering**
For each valid record, you need to calculate the difference (`delta`) between the current `value` and the *previous valid* `value` for that specific `sensor_id`. 
* Note: The first valid reading for any sensor does not have a previous value, so it does not produce a `delta`.
* Group your deltas by `sensor_id`.

**Step 5: Statistical Testing (Drift Detection)**
For each `sensor_id` that has at least 2 deltas (i.e., at least 3 valid records), calculate the 95% Confidence Interval for the mean of the `delta` values.
* Use the formula: `CI = mean +/- 1.96 * (std_dev / sqrt(N))`
* `N` is the number of deltas for that sensor.
* `std_dev` is the sample standard deviation of the deltas.
* A sensor is classified as "drifting" (1) if its 95% CI does **not** contain 0.0. Otherwise, it is "stable" (0).

**Step 6: Storage**
Create a SQLite database at `/home/user/features.db`.
Create a table named `sensor_stats` with the following schema:
`CREATE TABLE sensor_stats (sensor_id INTEGER PRIMARY KEY, n_deltas INTEGER, mean_delta REAL, ci_lower REAL, ci_upper REAL, is_drifting INTEGER);`

Insert a row for every `sensor_id` processed (that had at least 2 deltas). Ensure the values are inserted accurately.

Compile your C program as `/home/user/process_data` and run it to produce the SQLite database.