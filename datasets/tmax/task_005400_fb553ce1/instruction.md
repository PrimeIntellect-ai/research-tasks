You are a log analyst investigating a system that produces logs with multi-line messages (embedded newlines). You need to write a Go program to process this log file, calculate rolling statistics, and detect anomalies.

A log file is located at `/home/user/app.log`.
The log entries follow this format:
`[YYYY-MM-DD HH:MM:SS] LEVEL: Message...`

Because the `Message` part can contain embedded newlines, a log entry only ends when the next valid timestamp `[YYYY-MM-DD HH:MM:SS]` begins (or at the end of the file).

Write a Go program at `/home/user/analyze.go` and run it to produce a JSON file at `/home/user/anomalies.json`.

Your program must do the following:
1. Parse the file using regular expressions to correctly separate entries despite embedded newlines.
2. Extract the timestamp, the level, and the message content.
3. Compute the "message length" as the number of bytes in the extracted message. (Strip exactly one leading space right after the colon, but keep all other formatting, including newlines, in the message before measuring its length. Trim any trailing newlines from the very end of the extracted message block).
4. Maintain a rolling average of the message lengths of the *previous 3* valid entries. (Do not start checking for anomalies until you have at least 3 previous entries loaded into the rolling window).
5. An anomaly is detected if the current message length is **strictly greater than 2 times** the rolling average of the previous 3 message lengths.
6. Once an entry is evaluated, its length is added to the rolling window for future entries (even if it was an anomaly).
7. Output a JSON array containing the string timestamps of the anomalous entries in chronological order to `/home/user/anomalies.json`.

Example of the output format:
`["2023-10-01 10:00:25", "2023-10-01 10:01:10"]`

Execute your program to ensure the JSON file is generated successfully.