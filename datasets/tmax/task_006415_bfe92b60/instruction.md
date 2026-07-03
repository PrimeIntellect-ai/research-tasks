You are a log analyst investigating automated bot behavior. We are seeing bursts of highly similar API requests, but our logging system is noisy, and logs arrive slightly out of order. 

Your task is to create a Go-based log analysis pipeline that detects these anomalies and schedule it.

1. Write a Go program at `/home/user/detector.go` that reads a log file located at `/home/user/logs/raw.log`. 
2. The log file contains lines formatted as: `TIMESTAMP | IP | MESSAGE`
   * Timestamps are in RFC3339 format (e.g., `2023-10-25T14:30:00Z`), but lines might not be perfectly chronological.
3. Parse and sort the logs chronologically by timestamp.
4. For the `MESSAGE` portion of each log, normalize it by:
   * Converting to lowercase.
   * Removing all non-alphanumeric characters (replace them with spaces).
   * Tokenizing into a set of unique words.
5. Compute the Jaccard similarity between the normalized message sets of every *consecutive* pair of logs (after sorting chronologically). 
   * Jaccard similarity = (size of intersection) / (size of union).
6. Flag an "anomaly" if two consecutive logs occurred within `2.0` seconds of each other (inclusive) AND their Jaccard similarity is `>= 0.75`.
7. For every detected anomaly, append a line to `/home/user/anomalies.out` in the exact format:
   `[TIMESTAMP_1] and [TIMESTAMP_2] - Similarity: 0.XX`
   (where timestamps are the original RFC3339 strings, and similarity is formatted to exactly 2 decimal places, e.g., `0.80`).
8. Create a bash wrapper script at `/home/user/run_detector.sh` that compiles and runs your Go program. Make it executable.
9. Finally, add a user cron job that executes `/home/user/run_detector.sh` at the top of every minute (i.e., `* * * * *`).

Ensure you run your script once manually so that `/home/user/anomalies.out` is generated and populated with the current anomalies from the log file.