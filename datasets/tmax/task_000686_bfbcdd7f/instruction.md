You are acting as a log analyst investigating discrepancies between two independent tracking systems (Sensor A and Sensor B) monitoring the same object. Recently, we've noticed significant deviations in the reported positions, but the logs are difficult to compare directly due to different formats and slightly misaligned timestamps.

I need you to write a C++ program that processes these logs, aligns the events, calculates the positional discrepancy, and outputs anomalies.

Here are the details:
- You have two log files: `/home/user/sensor_a.log` and `/home/user/sensor_b.log`.
- `sensor_a.log` format: `[YYYY-MM-DD HH:MM:SS.mmm] INFO: Position detected at X=<val1> Y=<val2>`
  (e.g., `[2023-10-25 14:22:01.150] INFO: Position detected at X=12.5 Y=4.2`)
- `sensor_b.log` format: `[YYYY-MM-DD HH:MM:SS.mmm] TRACE: Object tracking - coord: (<val1>, <val2>)`
  (e.g., `[2023-10-25 14:22:01.180] TRACE: Object tracking - coord: (12.4, 4.3)`)

Your task:
1. Write a C++ program at `/home/user/analyze_logs.cpp` and compile it to `/home/user/analyze_logs`.
2. The program must read both log files and extract the timestamps and coordinates (X and Y). All logs occur on the same day: `2023-10-25`.
3. Align the data: For every entry in `sensor_a.log`, find the entry in `sensor_b.log` that has the *closest* timestamp. 
4. A pair is only valid if their timestamps differ by **100 milliseconds or less**. If no entry in B is within 100ms of an entry in A, ignore that entry from A. If multiple entries in B are equally close, pick the first one.
5. For each valid aligned pair, calculate the Euclidean distance between Sensor A's point (X_a, Y_a) and Sensor B's point (X_b, Y_b).
6. If the Euclidean distance is **strictly greater than 2.0**, it is considered an anomaly.
7. Write all anomalies to `/home/user/anomalies.csv` with the following header and CSV format:
   `timestamp_a,X_a,Y_a,timestamp_b,X_b,Y_b,distance`
   - Timestamps should be in the exact string format found in the brackets: `YYYY-MM-DD HH:MM:SS.mmm`
   - Coordinates and distance should be formatted to exactly 2 decimal places.

Execute your compiled program so that `/home/user/anomalies.csv` is populated correctly.