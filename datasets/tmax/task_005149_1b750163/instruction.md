You are an AI assistant helping a researcher organize their sensor datasets. We have a complex dataset ingestion pipeline where a video camera records an experiment, and multiple sensors write rapidly rotating logs. The start of the logs and the video are slightly out of sync.

Your task is divided into two parts:

**Part 1: Video Sync Analysis**
The raw video recording is located at `/app/dataset_recording.mp4`. 
The camera operator calibrates the start of the experiment by covering the lens, creating a sequence of completely black frames at the very beginning of the video. 
You must analyze the video and determine the `OFFSET`, which is defined as the exact number of completely black frames at the start of the video before the first non-black frame appears.

**Part 2: Log Transformation Script**
The sensors emit a high-speed stream of text logs. Because the logs rotate rapidly and sometimes get interrupted, the researcher needs a robust parsing script to normalize the data. 

There is a compiled reference binary at `/app/oracle_parser` which correctly parses the log stream. However, it is an older tool and the researcher needs it rewritten in Python for future integration.

You must create a Python script at `/home/user/log_parser.py`.
1. The script must take the `OFFSET` (the integer you found in Part 1) as its first command-line argument (e.g., `python3 /home/user/log_parser.py 42`).
2. The script must read raw log lines from `stdin` and write normalized lines to `stdout`.
3. Your Python script's behavior must be **bit-exact equivalent** to `/app/oracle_parser` for any given input and offset.

You should reverse-engineer the formatting, cleaning, and error-handling rules by feeding test inputs into `/app/oracle_parser <offset>` and observing its output. The logs generally contain event IDs, timestamps, and payload data, alongside occasional rotation markers and noise.

**Constraints & Requirements:**
- You must write your final script to `/home/user/log_parser.py`.
- Use Python 3.
- Standard libraries only. `ffmpeg` is available on the system for video analysis.
- Your script will be aggressively fuzzed against the oracle with thousands of synthetic log lines to verify correctness.