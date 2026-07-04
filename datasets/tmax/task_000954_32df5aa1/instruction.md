You are a data engineer building a Rust-based ETL pipeline for a smart city traffic analysis system. We have irregular GPS ping data from a public bus and a list of fixed traffic monitoring points.

Your objective is to write a Rust program that extracts this data, aligns and interpolates the irregular timestamps into regular intervals, calculates the distance to the monitoring points, and exports a bulk SQL insert script for a database.

Here are the requirements:

1. **Setup Project**: Create a new Rust project in `/home/user/traffic_etl`. You may use external crates like `chrono`, `csv`, or `serde`.
2. **Read Inputs**:
   - Bus GPS data: `/home/user/data/bus_gps.csv` (Columns: `timestamp,bus_id,x,y`) - Timestamps are in ISO 8601 UTC format.
   - Target points: `/home/user/data/targets.csv` (Columns: `point_id,x,y`)
3. **Transform & Interpolate**:
   - The GPS pings are irregular. You must align the data to strict 10-second intervals (e.g., `...:00Z`, `...:10Z`, `...:20Z`, etc.).
   - Find the minimum and maximum timestamps for the bus in the dataset. For every 10-second aligned interval `T` between the minimum and maximum timestamp (inclusive of boundaries if they fall exactly on a 10s interval), linearly interpolate the `x` and `y` coordinates of the bus.
   - To interpolate for an aligned time `T`, find the exact closest data points `T_prev` and `T_next` such that `T_prev <= T <= T_next`. If `T` exactly matches a timestamp in the data, use those coordinates.
4. **Calculate Distance**:
   - For each interpolated 10-second point, calculate the Euclidean distance to all target points in `targets.csv`.
5. **Bulk Export**:
   - Filter out any pairs where the distance is strictly greater than `50.0`.
   - For the remaining pairs, generate a file at `/home/user/etl_output.sql` containing bulk SQL insert statements in exactly this format (one per line, ordered chronologically):
     `INSERT INTO bus_proximity (timestamp, bus_id, point_id, distance) VALUES ('YYYY-MM-DDTHH:MM:SSZ', 'bus_id', 'point_id', <distance_rounded_to_2_decimal_places>);`

**Constraints**:
- Use standard linear interpolation: `val = val1 + (val2 - val1) * (T - T1) / (T2 - T1)` (where `T` is Unix timestamp in seconds).
- Round the final distance to exactly 2 decimal places in the SQL string (e.g., `40.00`).
- Do not generate intervals outside the `T_min` and `T_max` of the bus data.
- Run the program so that `/home/user/etl_output.sql` is generated.