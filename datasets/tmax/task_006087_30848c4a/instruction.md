As an automation specialist, you need to create a high-performance log processing pipeline to detect CPU usage anomalies in a server farm. The server logs are massive, so the processing must be done efficiently in C++ without loading the entire file into memory (streaming approach).

The input data will be located at `/home/user/server_metrics.log`.
Each line of the log follows this exact format:
`[YYYY-MM-DD HH:MM:SS] INFO - CPU: <value>% RAM: <value>MB STATUS: <string>`
Example:
`[2023-10-01 10:00:05] INFO - CPU: 21.5% RAM: 2048MB STATUS: OK`

Your task:
1. Write a C++ program at `/home/user/anomaly_detector.cpp` that streams `/home/user/server_metrics.log` line-by-line.
2. The program must extract the timestamp (e.g., `2023-10-01 10:00:05`) and the CPU percentage as a floating-point number.
3. Implement a simple moving average (SMA) anomaly detector with a window size of exactly 50. 
   - The SMA for the current line is calculated strictly from the CPU values of the *previous* 50 lines.
   - You only begin checking for anomalies on the 51st line (once the window is full).
   - An anomaly is triggered if the current line's CPU usage is strictly greater than `2.0 * SMA`.
4. Whenever an anomaly is detected, the program must append a line to `/home/user/anomalies.csv` in this exact format:
   `YYYY-MM-DD HH:MM:SS,<Current_CPU>,<SMA>`
   (Format floats to exactly 1 decimal place, e.g., `2023-10-01 12:05:00,88.8,22.0`).
5. Create a shell script at `/home/user/run_pipeline.sh` that orchestrates this workflow:
   - Compiles `/home/user/anomaly_detector.cpp` into an executable named `/home/user/detector` using `g++` with `-O3` optimization.
   - Executes `/home/user/detector`.
   - Counts the total number of lines in `/home/user/anomalies.csv` and saves this integer to `/home/user/anomaly_count.txt`.

Constraints:
- Do not load the entire log file into memory. Read it streamingly.
- Write your own simple rolling window logic; do not rely on external statistical libraries.
- The output CSV must not have a header line.