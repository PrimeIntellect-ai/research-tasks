You are acting as a DevOps engineer investigating a critical system failure. You have two objectives: analyze the console output from the crash, and fix the log parsing utility that is currently failing on the corrupted logs.

**Part 1: Video Analysis**
The only surviving record of the system panic is a video recording of the console output, located at `/app/console_panic.mp4`.
Analyze this video (you may use `ffmpeg` to extract frames or use OCR tools like `tesseract`) to find the final panic code. Somewhere in the video, the text `Kernel Panic Code: <HEX_CODE>` is displayed.
Extract this hexadecimal code and save it into a file at `/home/user/panic_code.txt` (the file should contain only the hex code, e.g., `0x1234ABCD`).

**Part 2: Log Parser Debugging**
You have the source code for the team's custom log parser at `/home/user/log_parser.c`. The parser reads log entries from `stdin` (line by line) and prints parsed details to `stdout`. 
A valid log line format is strictly: `[<timestamp>] <LEVEL>: <message>`
Where:
- `<timestamp>` is any string of characters not containing `]`.
- `<LEVEL>` is any string of characters not containing `:`.
- `<message>` is the rest of the line (excluding the leading space after the colon).

For valid lines, the parser should output:
`Parsed: <LEVEL> | <message>`
For invalid lines (missing brackets, missing colon, corrupted format), the parser should output:
`INVALID`

Currently, `log_parser.c` crashes with memory corruption and segmentation faults when it encounters unexpectedly formatted or corrupted input (e.g., missing brackets, extremely long messages, or unexpected characters). 
Your task is to:
1. Debug the `log_parser.c` program using `gdb` or tracebacks to understand the crashes.
2. Fix the corrupted input handling so that the program NEVER crashes, regardless of the input.
3. Ensure the parsing logic strictly adheres to the output format above. Maximum expected line length is 1024 bytes, but your program should gracefully output `INVALID` for lines exceeding this without crashing.
4. Compile your fixed program to `/home/user/log_parser` (e.g., `gcc -O2 /home/user/log_parser.c -o /home/user/log_parser`).

The automated test will rigorously test your compiled binary against millions of mutated and corrupted strings to ensure no crashes occur and the output perfectly matches the reference implementation.