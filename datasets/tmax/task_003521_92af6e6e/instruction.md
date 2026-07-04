You are a data scientist tasked with cleaning and analyzing data from two environmental sensors that have been reporting temperature readings at irregular intervals. Your goal is to detect if there is a "drift" (divergence) between the two sensors over time.

You must write a C++ program that reads the raw data, aligns it to a common timeline, handles missing values, normalizes the signals, and computes the Euclidean distance between them.

The input datasets are located at:
- `/home/user/sensor_a.csv`
- `/home/user/sensor_b.csv`

Both CSV files have headers: `timestamp,temperature`. The `timestamp` is an integer representing UNIX epoch seconds. The `temperature` is a floating-point number.

Your C++ program must be saved at `/home/user/drift_analyzer.cpp`, compiled to `/home/user/drift_analyzer` using `g++`, and when run, it should produce an output file at `/home/user/drift_report.txt`.

Perform the following data processing steps in your C++ program:
1. **Time-based Bucketing**: Find the global minimum timestamp and global maximum timestamp across *both* datasets. Round the global minimum down to the nearest multiple of 600 (10 minutes) to get your `start_time`. Round the global maximum up to the nearest multiple of 600 to get your `end_time`.
2. **Aggregation**: Divide the time range `[start_time, end_time)` into consecutive 600-second buckets. For each bucket and for each sensor, calculate the mean temperature of all readings that fall strictly within that bucket `[bucket_start, bucket_end)`.
3. **Gap-Filling**: If a sensor has no readings in a bucket:
   - Forward-fill: Use the final aggregated value from the immediately preceding bucket.
   - Backward-fill (for leading gaps): If the very first bucket(s) are empty, fill them with the aggregated value of the first bucket that *does* have data for that sensor.
4. **Standardization**: Separately for Sensor A and Sensor B, normalize the complete sequence of bucket values using Z-score standardization: `z = (x - mean) / std_dev`. Use the population standard deviation (divide by N). If the standard deviation is 0, the normalized values should all be 0.
5. **Distance Computation**: Calculate the Euclidean distance between the normalized bucket array of Sensor A and the normalized bucket array of Sensor B.

The output file `/home/user/drift_report.txt` must contain exactly two lines:
```
Total Buckets: <integer>
Euclidean Distance: <float>
```
The Euclidean Distance must be rounded to exactly 4 decimal places.