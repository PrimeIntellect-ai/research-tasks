You are a data scientist cleaning a large dataset of high-frequency sensor telemetry. Because of performance constraints, you need to implement the data cleaning and aggregation pipeline in C.

A binary file containing the raw sensor data is located at `/home/user/telemetry.bin`. 
The file contains a sequence of binary records (little-endian). Each record is 16 bytes and consists of the following C struct layout:
```c
struct Record {
    int32_t ts;    // timestamp in seconds
    float x;       // x coordinate
    float y;       // y coordinate
    float val;     // sensor reading
};
```

Your task is to write a C program at `/home/user/clean.c`, compile it to `/home/user/clean` (ensure you link `libm` and enable OpenMP with `-fopenmp`), and run it to produce a cleaned, aggregated CSV file at `/home/user/summary.csv`.

The C program must perform the following pipeline:
1. **Data I/O:** Read all records from `/home/user/telemetry.bin` into memory.
2. **Distance Filtering & Parallel Processing:** Using OpenMP (`#pragma omp parallel for`), iterate over the records and flag or filter out anomalous readings. A reading is an anomaly and should be ignored if its Euclidean distance from the origin (0.0, 0.0) is strictly greater than `100.0`.
3. **Time-based Bucketing:** Group the *valid* records into 10-second time buckets based on their timestamp. A bucket's identifier is `(ts / 10) * 10`. Compute the average `val` for all valid records in each bucket.
4. **Windowed Rolling Aggregation:** For each bucket (sorted chronologically), compute a rolling average of the bucket averages over a window of size 2. (i.e., the rolling average for bucket $N$ is the average of the bucket average of $N$ and the bucket average of $N-1$. For the very first chronological bucket, the rolling average is just its own bucket average). *Note: Only consider buckets that contain at least one valid record.*
5. **Output:** Write the results to `/home/user/summary.csv`. The CSV must have a header and match this format exactly:
```csv
bucket,bucket_avg,rolling_avg
1000,45.21,45.21
1010,48.00,46.61
...
```
Print all floating-point numbers to exactly two decimal places (`%.2f`). Ensure the rows are sorted by `bucket` in ascending order.