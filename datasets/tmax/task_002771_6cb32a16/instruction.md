You are a log analyst investigating sudden spikes in error rates on a legacy system. The system produces massive log files, but a recent misconfiguration caused binary garbage to be injected into the log streams, corrupting the text encoding.

Your task is to write a C program that streams a large log file, sanitizes the character encoding, detects the first anomaly (error spike), and generates a summary report from a template.

Here are the specific requirements:

1. **Input Files**:
   - `/home/user/system_logs.dat`: The raw, corrupted log file. Each line starts with a timestamp in brackets, e.g., `[1620000000] INFO Operation successful.` or `[1620000010] ERROR Connection timeout.`. Some lines contain non-printable binary garbage.
   - `/home/user/report_template.txt`: A text template containing placeholders `{{FIRST_ANOMALY_TIMESTAMP}}` and `{{TOTAL_ERRORS}}`.

2. **C Program Execution**:
   - Write your code in `/home/user/log_analyzer.c`.
   - The program must process `/home/user/system_logs.dat` line-by-line (streaming). Do not read the entire file into memory at once.
   
3. **Data Sanitization**:
   - Clean the incoming stream: Strip out any byte that is not a standard printable ASCII character (hex 0x20 to 0x7E) EXCEPT for the newline (`\n`, hex 0x0A) and carriage return (`\r`, hex 0x0D).
   - After stripping the bad bytes, process the sanitized line.

4. **Anomaly Detection**:
   - Maintain a rolling window of the last 100 sanitized log lines.
   - An "anomaly" is triggered if there are **20 or more** lines containing the substring `] ERROR ` within the current 100-line window.
   - You only need to find the **first** anomaly. Record the timestamp (the integer inside the brackets `[]`) of the log line that caused the window's error count to hit 20.

5. **Template-Based Output**:
   - Track the total number of `ERROR` lines across the entire file.
   - After processing the whole file, read `/home/user/report_template.txt`.
   - Replace `{{FIRST_ANOMALY_TIMESTAMP}}` with the exact timestamp of the first anomaly. (If no anomaly is found, use `NONE`).
   - Replace `{{TOTAL_ERRORS}}` with the total count of error lines in the entire log.
   - Write the finalized text to `/home/user/anomaly_report.txt`.

6. **Compilation and Execution**:
   - Compile your program using `gcc -O2 /home/user/log_analyzer.c -o /home/user/log_analyzer`.
   - Run the executable so that `/home/user/anomaly_report.txt` is generated.