I am a log analyst investigating a sudden performance degradation in our web services. I need you to help me find exactly when the anomaly started by processing our archived logs.

Here is your task:

1. **Local Data Transfer:** I have a set of archived log files located in `/home/user/log_archive`. Create a working directory at `/home/user/workspace` and copy all `.log` files from the archive into this workspace.

2. **Data Format & Encoding:** 
   - The log files are encoded in **UTF-16LE**. 
   - Each line in the logs represents a single request and uses the pipe `|` character as a delimiter. 
   - The format is: `YYYY-MM-DD HH:MM:SS|IP_ADDRESS|STATUS_CODE|RESPONSE_TIME_MS`
   - Example (when decoded): `2023-10-27 14:32:05|192.168.1.50|200|145`

3. **C Program Implementation:**
   Write a C program at `/home/user/workspace/detector.c`. The program must:
   - Accept a variable number of log file paths as command-line arguments.
   - Use POSIX threads (`pthreads`) to process multiple log files in parallel (one thread per file is acceptable).
   - Handle the character encoding (read the UTF-16LE files and process the text).
   - Extract the timestamp (down to the minute, i.e., `YYYY-MM-DD HH:MM`) and the `RESPONSE_TIME_MS` (integer).
   - Aggregate the data to calculate the average response time for each minute across all processed files.
   - Detect the **changepoint/anomaly**: identify the *earliest* minute (chronologically) where the average response time across all logs is strictly greater than `500` ms.

4. **Output:**
   Once the program identifies the anomalous minute, it must write exactly one line to `/home/user/anomaly.txt` in the following format:
   `ANOMALY_DETECTED: YYYY-MM-DD HH:MM`

Compile your program (e.g., `gcc -pthread detector.c -o detector`), run it against the logs in your workspace, and ensure `/home/user/anomaly.txt` is generated correctly.