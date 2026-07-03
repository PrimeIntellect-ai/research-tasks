You are a localization engineer processing translated subtitles and voiceover cues. You have been provided with an English reference audio file at `/app/audio/ref.wav`.

You receive batch translation files in JSON-Lines format. Unfortunately, the external translation vendor's tool is buggy and occasionally generates anomalous data. Specifically, it sometimes produces:
1. **Malformed Unicode Escapes:** Occurrences of `\u` that are NOT immediately followed by exactly 4 valid hexadecimal digits (`0-9`, `a-f`, `A-F`). 
2. **Timing Anomalies:** Lines where the `start_ts` is greater than or equal to `end_ts`, or where the `end_ts` exceeds the total duration of the reference audio file by more than 0.1 seconds.

Your task is to build a high-performance filter in **C** to detect these broken files.

**Requirements:**
1. Determine the exact duration of `/app/audio/ref.wav` in seconds (you may use tools like `ffprobe` or `sox`).
2. Write a C program at `/home/user/loc_filter.c` and compile it to `/home/user/loc_filter`.
3. The program must accept the audio duration as its first command-line argument: `./loc_filter <max_duration_in_seconds>`.
4. It must read a JSON-Lines file from `stdin`. Each line contains a JSON object with at least `"start_ts": <float>` and `"end_ts": <float>`. (You do not need a full JSON parser; simple string matching or `sscanf` logic is sufficient for the timestamps, but beware of arbitrary spacing).
5. The program must scan the entire raw input for malformed unicode escapes.
6. If **any** timing anomaly or malformed unicode escape is found in the input stream, the program must immediately print `REJECT` to `stdout` and exit with status code `1`.
7. If the entire file is processed and no anomalies or malformed escapes are found, it must print `ACCEPT` to `stdout` and exit with status code `0`.

To help you validate your program, we have provided two corpora of `.jsonl` files:
- `/app/corpus/clean/`: Contains perfectly valid localization files. Your program MUST accept 100% of these.
- `/app/corpus/evil/`: Contains files with sneaky timing anomalies or broken unicode sequences. Your program MUST reject 100% of these.

Ensure your C code is efficient and handles memory safely. Do not use external C libraries beyond the standard library (libc).