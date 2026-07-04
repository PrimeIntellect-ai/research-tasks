You are a mobile build engineer tasked with fixing and improving the CI pipeline's log processing and UI test analysis stages. Perform the following three tasks:

**Task 1: Fix the C Log Processor**
There is a legacy C program used to preprocess raw logs located in `/home/user/log_tool/`.
The `Makefile` is broken due to syntax errors (likely spaces instead of tabs) and a missing output flag.
Fix the `Makefile` and successfully compile the program so that the executable `/home/user/log_tool/log_processor` is created.

**Task 2: Write a Go Log Sanitizer**
We need a robust log sanitizer to prevent pipeline injection attacks and encoding errors. 
Write a Go program at `/home/user/sanitizer.go`. It must take a single file path as a command-line argument:
`go run /home/user/sanitizer.go <path_to_file>`

The program must parse the file and enforce the following strict encoding rules:
1. The file must be 100% valid UTF-8.
2. The file must NOT contain any ASCII control characters (characters in the range 0x00 to 0x1F, or 0x7F), EXCEPT for tab (`\t`), newline (`\n`), and carriage return (`\r`).
3. No single line (delimited by `\n`) may exceed 2000 bytes in length.

If the file violates ANY of these rules, the program must immediately print an error and exit with status code `1` (Reject).
If the file strictly adheres to all rules, the program must exit with status code `0` (Accept).

**Task 3: UI Test Video Analysis**
Our automated mobile UI tests record a video of the screen. If a fatal crash occurs, the test runner flashes a completely solid Red screen (RGB: 255, 0, 0) for exactly one frame.
You have been provided with a test recording artefact at `/app/test_run.mp4`.
Use `ffmpeg` to extract the frames and analyze them to find the 1-based frame index of the first pure red frame. 
Write ONLY the integer frame number to `/home/user/red_frame.txt`.

Ensure your Go program is highly performant and handles edge cases, as it will be tested against a hidden adversarial corpus of clean and malicious logs.