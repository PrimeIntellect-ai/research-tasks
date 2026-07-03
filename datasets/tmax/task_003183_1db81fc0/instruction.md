I am an automation specialist building a new ETL pipeline for IoT sensor data. I need you to write a C program that processes raw telemetry data, applying time-based bucketing, spatial distance calculations, and rolling statistics.

You have been provided a dataset at `/home/user/sensor_data.csv`.
The CSV has no header and contains four columns: `timestamp,x_coord,y_coord,signal_strength`.
- `timestamp`: integer (seconds)
- `x_coord`: float
- `y_coord`: float
- `signal_strength`: float

Please write a C program at `/home/user/processor.c`, compile it to `/home/user/processor`, and execute it to generate an output file at `/home/user/processed_stats.csv`.

Your C program must perform the following operations:
1. **Time-based Bucketing**: Group the rows into 10-second buckets based on the `timestamp`. A bucket's key is calculated as `(timestamp / 10) * 10` (using integer division). 
2. **Aggregation & Distance Computation**: For each bucket, calculate the mean `x_coord` and mean `y_coord`. Then, calculate the Euclidean distance of this centroid (mean X, mean Y) from the origin (0.0, 0.0). 
3. **Rolling Statistics**: Compute a simple moving average (SMA) of the centroid distances using a window size of 3 buckets. 
   - For the first bucket, the rolling average is just its own distance.
   - For the second bucket, it's the average of the first two buckets' distances.
   - For the third bucket and beyond, it is the average of the current bucket's distance and the previous two buckets' distances.
   - Note: The window applies to the sequence of *present* buckets in the data, sorted chronologically. You can assume the input data is already sorted by timestamp.

**Output Format:**
Write the results to `/home/user/processed_stats.csv`.
Include a header row exactly as: `bucket_time,centroid_distance,rolling_avg_distance`
Format the floating-point numbers to exactly two decimal places (e.g., `%.2f`).
Each line should look like: `1000,5.00,5.00`

Ensure your C code is robust, correctly handles file I/O, and relies on the standard math library (remember to link with `-lm` if necessary).