You are an IT support technician investigating a priority ticket (#992). A legacy reporting job failed, and the development team needs to know exactly when it crashed and what the underlying error was.

You have been provided with a mixed service log file located at `/home/user/logs/services.log`. This log contains entries from two different services (`app` and `formatter`) that inexplicably use different timestamp formats (Unix epoch and ISO-8601). 

When the `formatter` service crashes, the `app` service catches the exit code and dumps the formatter's raw error memory buffer as a hex-encoded string in the log.

Your tasks are to:
1. Reconstruct the log timeline to find the exact Unix epoch timestamp of the `ERROR` log entry. (You'll need to handle the mixed timestamp formats).
2. Extract the hex-encoded payload from that `ERROR` line.
3. Decode the hex payload into readable ASCII text to reveal the hidden error message.
4. Create a resolution file at `/home/user/ticket_992_resolution.txt` containing exactly one line with the epoch timestamp of the crash and the decoded error message, separated by a hyphen and spaces.

Format of `/home/user/ticket_992_resolution.txt`:
`<EPOCH_TIMESTAMP> - <DECODED_ERROR_MESSAGE>`

Example output format:
`1698825615 - Segment fault at 0x08`

You may use standard Linux shell utilities to solve this.