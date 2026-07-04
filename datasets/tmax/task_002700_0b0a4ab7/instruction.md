You are an IT support technician investigating a series of escalating helpdesk tickets regarding corrupted data processing logs. 

A legacy system relies on a proprietary, stripped binary located at `/app/data_ingest` to process incoming JSON log streams. Recently, it was discovered that this binary occasionally goes rogue—it deletes the original incoming log files to cover its tracks and injects subtle, malicious anomalies into the output stream. 

Your tasks are to:
1. Use system call tracing (e.g., `strace`) and reverse engineering (or fuzzing) on the `/app/data_ingest` binary to understand exactly how it mutates the logs and what statistical anomalies or patterns define a "corrupted" (evil) log entry.
2. Recover or reconstruct the timeline of events to understand the baseline statistics of clean logs versus the malicious injections.
3. Write a Python script at `/home/user/sanitize.py` that acts as a definitive classifier.

**Requirements for `/home/user/sanitize.py`:**
- It must be an executable Python 3 script.
- It will be invoked from the command line with a single argument: the path to a text file containing one JSON log entry per line.
- Example invocation: `python3 /home/user/sanitize.py /path/to/logs.txt`
- For *each line* in the input file, your script must print exactly one word to standard output: `CLEAN` if the log is untouched, or `EVIL` if it contains the anomalies injected by the rogue binary.
- Do not print any other text, warnings, or debug information to standard output. 

You must ensure your script perfectly separates legitimate logs from corrupted ones. To help you develop your logic, you can analyze the behavior of `/app/data_ingest` by feeding it sample JSON strings and observing its output and system calls.