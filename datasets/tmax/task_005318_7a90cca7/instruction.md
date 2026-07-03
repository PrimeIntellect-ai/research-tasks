You are a monitoring specialist taking over for a colleague who left abruptly. They left a voicenote detailing the parameters for a new storage monitoring alert system. You need to complete the setup based on their instructions and rewrite a legacy C-based log parsing tool.

Here are your instructions:
1. **Transcribe the Voicenote**: You will find an audio file at `/app/voicenote.wav`. You may use any available tools (like `ffmpeg` and `whisper.cpp`, which are installed in the environment) to transcribe it. The voicenote contains the required quota threshold percentage, the specific port you need to forward, and the directory path you must mount.
2. **Setup the Filesystem**: Create a dummy filesystem image using `mksquashfs` of your `/home/user/.profile` (just to have some data) and mount it using `squashfuse` to the exact directory path specified in the voicenote.
3. **Configure Port Forwarding**: Use `socat` to forward local TCP port 9090 to the port specified in the voicenote. Run this in the background.
4. **Implement the Alert Parser (C)**:
    - There is a legacy compiled binary at `/app/oracle_parser` that processes storage metrics logs from `stdin` and writes formatted alerts to `stdout`.
    - You must write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`.
    - Your program must behave *exactly* like `/app/oracle_parser` for any given input. 
    - The input format consists of lines with the format: `DEVICE_NAME BYTES_USED BYTES_TOTAL` (e.g., `sda1 860 1000`).
    - If the percentage used (BYTES_USED / BYTES_TOTAL * 100, integer division) is STRICTLY GREATER than the threshold mentioned in the voicenote, the program should output: `ALERT: [DEVICE_NAME] usage is [PERCENT]%` followed by a newline.
    - Invalid lines or lines below/equal to the threshold should produce no output.
    - Your compiled binary `/home/user/parser` will be strictly fuzzed against `/app/oracle_parser` to ensure bit-exact equivalence.
5. **Scheduled Task**: Add an entry to your user crontab that runs `/home/user/parser` every 5 minutes, though the automated test will strictly rely on fuzzing your compiled binary directly.