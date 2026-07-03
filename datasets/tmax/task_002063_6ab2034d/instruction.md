You are a data analyst troubleshooting a broken ETL pipeline that processes CSV files from IoT sensors. The pipeline retries on failure, which introduces duplicate records. Furthermore, occasional sensor dropouts result in missing values (represented as `-1`), and the data is currently in a wide format rather than the required long format.

Your task is to write a C program that acts as a standard UNIX filter (reading from `stdin` and writing to `stdout`) to clean, transform, and reshape this data.

First, you need a calibration key. We have a video recording of the ETL dashboard at `/app/dashboard.mp4`. Find out the exact total number of frames in this video. Let this integer be `F`.

Write a C program at `/home/user/etl_fix.c` and compile it to an executable named `/home/user/etl_fix`.

The program must perform the following operations on a CSV stream:
1. **Input Format:** The input has a header `time,s1,s2,s3` followed by rows of integers. Missing values are denoted by `-1`.
2. **Hash-based Deduplication:** The ETL job frequently duplicates rows. Track the `time` field to drop duplicates. Use a simple hash table of size 1024 (using `time % 1024` as the index). If a `time` value maps to an occupied slot with the exact same `time`, ignore the entire row. Otherwise, overwrite the slot with the new `time` and process the row.
3. **Imputation:** For any sensor value (`s1`, `s2`, or `s3`) that is `-1`, perform a forward-fill by replacing it with the most recent valid (or previously imputed) value for that specific sensor. If no previous valid value exists (i.e., it's the beginning of the stream), leave it as `-1`.
4. **Feature Transform:** For any sensor value that is NOT `-1` (after imputation), apply a bitwise XOR with the video frame count `F`.
5. **Wide-to-Long Reshaping:** For every processed (non-duplicate) row, output three lines in long format: `time,sensor_name,value`. The sensor names are `s1`, `s2`, and `s3`.

**Example Input:**
```
time,s1,s2,s3
100,50,-1,20
100,50,-1,20
105,-1,30,-1
```

**Example Output (Assuming F=142):**
```
100,s1,176
100,s2,-1
100,s3,154
105,s1,176
105,s2,184
105,s3,154
```
*(Explanation: 100 is processed. 50 XOR 142 = 176. The second row is a duplicate. In the third row, s1 is forward-filled to 50, s3 is forward-filled to 20, then XORed).*

Compile your C code without any external libraries (standard C library only). Automated tests will stream thousands of randomized CSVs to your compiled `/home/user/etl_fix` binary to verify bit-exact behavioral equivalence.