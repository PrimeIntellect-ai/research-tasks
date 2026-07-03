A junior DevOps engineer accidentally deleted a critical system trace log and then ran a buggy script that caused our log processing pipeline to hang. We need you to step in, perform forensic recovery, and fix the processing pipeline.

Here is the situation:
1. **Forensics**: We have a raw ext4 disk image located at `/home/user/logs.img`. The deleted file was named `trace.log`. You need to recover this file from the image.
2. **Stripped Binary**: To be accepted by our central logging server, every line in the log must be signed. We have a proprietary binary at `/app/sign_log` that takes a log string as an argument and prints the correct checksum signature. The binary is stripped.
3. **C Code Debugging**: We have a buggy recovery tool at `/home/user/repair.c`. It is supposed to read the recovered `trace.log`, filter out garbled or empty lines, and append the correct signature to each valid line (either by calling the binary or implementing its logic). 
   - Unfortunately, `repair.c` currently suffers from an off-by-one memory error that causes a segmentation fault on long lines.
   - It also has a convergence failure (infinite loop) when it encounters lines with consecutive delimiter characters.
   
Your task:
1. Recover `trace.log` from `/home/user/logs.img`.
2. Debug and fix `/home/user/repair.c` so it can cleanly process the recovered log.
3. Use the fixed `repair.c` (and optionally `/app/sign_log`) to generate the final signed log file at `/home/user/final_trace.log`.

The final output `/home/user/final_trace.log` must contain the recovered log lines, one per line, formatted exactly as:
`<original log line text>|<signature>`

Generate as many valid, correctly signed lines as possible. Our automated systems will score your `final_trace.log` based on the percentage of correctly recovered and signed lines.