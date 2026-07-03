You have inherited an unfamiliar codebase for a custom log analysis tool written in C. The source code is located at `/home/user/log_analyzer.c`.

The tool reads binary event logs. Most logs process perfectly, but occasionally the program crashes with a Segmentation Fault when processing certain files. The previous developer mentioned that the failure seems intermittent and likely relates to how specific edge-case event lengths are handled during parsing, but they didn't finish intermediate state tracing to find the exact root cause.

Your task:
1. Investigate `/home/user/log_analyzer.c` and find the bug. Pay close attention to how the format parsing handles edge-cases with record lengths.
2. Fix the bug in `/home/user/log_analyzer.c`. Your fix must allow the program to safely process any validly structured event (even if its length is large) without crashing or corrupting memory. If a type 1 event's length is 64 or greater, dynamically allocate memory to read it safely instead of using the fixed-size buffer, or truncate it safely. Ensure no memory leaks are introduced.
3. Compile your fixed version to `/home/user/log_analyzer_fixed` (use `gcc /home/user/log_analyzer.c -o /home/user/log_analyzer_fixed`).
4. Run your fixed program on the provided log file `/home/user/data/event_log.bin`.
5. The program outputs a final summary line: `Processed X events, Type1 length sum: Y`. Pipe or redirect this exact single line of output into `/home/user/result.txt`.

Ensure `/home/user/result.txt` contains only the output line from the fixed program running on `event_log.bin`.