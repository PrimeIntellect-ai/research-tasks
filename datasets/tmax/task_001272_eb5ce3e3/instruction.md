You are acting as a performance engineer responsible for profiling a distributed microservice architecture. 

We have two tasks for you to complete. 

**Part 1: Video Observational Data Reshaping**
A recent incident was captured in a screen recording of our legacy dashboard, located at `/app/incident_dashboard.mp4`. The dashboard shows a status indicator in the top-left corner (the region is exactly the top-left 50x50 pixels). When the system experiences a "Global Sync" event, this indicator flashes pure white. 
Your task is to extract the timestamps of these Global Sync events. 
1. Use `ffmpeg` to process the video and extract the frames or analyze the video filters. 
2. Identify the frames where the average brightness of the top-left 50x50 pixel region exceeds a grayscale value of 200.
3. Save the timestamps (in seconds, accurate to 2 decimal places) of these frames to `/home/user/sync_events.txt`, with one timestamp per line.

**Part 2: Adversarial Graph Anomaly Detector**
The system's tracing logs record microservice interactions. A known performance degradation is caused by an architectural violation where a temporary cycle forms in the call graph.
We have collected a corpus of trace logs. Some represent healthy traffic, and some contain the "evil" performance anomalies. 
The logs are formatted as space-separated columns: `[Timestamp_Integer] [Source_Node] [Destination_Node] [Latency_ms]`

You must write a Bash script at `/home/user/detect_anomaly.sh` that takes a single trace log file path as its first argument.
Your script must:
1. Parse the log file using only Bash built-ins, `awk`, `grep`, or other standard POSIX coreutils.
2. Act as a classifier. A log is considered "anomalous" (evil) if and only if it contains a structural cycle of length 3 (e.g., Node X -> Node Y, Node Y -> Node Z, Node Z -> Node X) occurring within the same timestamp window (the integer `Timestamp_Integer` is identical for all three calls).
3. Exit with code `0` if the log is completely clean (no cycles of length 3 within any single timestamp).
4. Exit with code `1` if the log is anomalous (contains at least one cycle of length 3 within a single timestamp).

Your script will be tested against an adversarial test suite. It must correctly reject 100% of the evil logs (exit 1) and preserve 100% of the clean logs (exit 0).

Ensure your script is executable (`chmod +x /home/user/detect_anomaly.sh`).