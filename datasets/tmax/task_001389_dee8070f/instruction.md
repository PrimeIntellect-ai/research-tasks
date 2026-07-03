You are an engineer investigating a long-running data pipeline script `/home/user/process_broadcast.sh` that extracts and concatenates audio segments from a daily broadcast recording `/app/radio_broadcast.wav` based on a log of timestamps (`/home/user/segments.log`).

Currently, the script is failing its quality checks and timing out. There are three identified issues:
1. **Precision loss and Timezone bug:** The current script tries to parse the ISO8601 timestamps using `date +%s`, which drops fractional seconds and mishandles certain timezone offsets. As a result, the start times and durations for `ffmpeg` extraction are rounded to integers, leading to misaligned audio snippets that chop off words.
2. **Format parsing edge-case repair:** The log file (`segments.log`) occasionally contains malformed timezone suffixes or missing decimal seconds that break the simplistic parsing logic.
3. **Performance bottleneck / Memory issue:** The script currently invokes `ffmpeg` iteratively in a Bash `while` loop, reloading the large audio file for every single segment. This acts like a memory/resource leak over time and makes processing extremely slow.

Your task is to debug and rewrite `/home/user/process_broadcast.sh` so that it:
- Accurately parses the start and end times from `/home/user/segments.log` into exact fractional seconds relative to the start of the audio file.
- The audio file `/app/radio_broadcast.wav` begins exactly at `2023-10-27T00:00:00Z`. (i.e., time `0.0` in the WAV corresponds to this UTC time).
- Efficiently extracts and concatenates these segments into a single output file at `/home/user/final_output.wav` without precision loss. You should optimize the data transformation to avoid invoking `ffmpeg` hundreds of times independently if possible, or use an efficient stream-copying approach.

You must write your solution primarily in Bash (modifying `process_broadcast.sh`), though you may use standard tools like `awk`, `python3`, or `bc` within the script to handle the math and precision.

Ensure your final script produces the corrected concatenated audio at `/home/user/final_output.wav`.