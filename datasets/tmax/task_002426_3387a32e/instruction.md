You are a support engineer investigating an intermittent crash in our C++ orbital sensor telemetry pipeline. Customers are reporting that the sensor processing module occasionally panics due to a catastrophic precision loss (resulting in `NaN`s) in the angular velocity calculations. 

A field technician left an audio diagnostic message containing clues about the failure conditions. You will find this recording at `/app/support_voicemail.wav`.

Your task is to:
1. Transcribe and analyze the audio file to determine the exact conditions (the bounds of the angular velocity `x`) that trigger the precision loss.
2. Review the provided sensor math library at `/home/user/sensor_math.cpp` to understand how the formula `(1 - cos(x)) / (x * x)` is currently implemented and why it suffers from catastrophic cancellation within those bounds.
3. Create a C++ diagnostic filter tool to triage customer log files. Write your code in `/home/user/triage_logs.cpp` and compile it to `/home/user/triage_logs`.

**Requirements for the Triage Tool:**
- The tool must take a single command-line argument: the absolute path to a CSV log file.
- The CSV files have no headers and contain a single column of floating-point angular velocity values (`x`).
- Your tool must read the file and determine if it contains any values that fall strictly within the failure bounds specified in the audio message.
- If the file contains one or more failing values, the tool MUST print exactly `EVIL` to standard output and exit with code `1`.
- If the file does NOT contain any failing values, the tool MUST print exactly `CLEAN` to standard output and exit with code `0`.
- The tool must be efficient and handle large CSV files.

You may install any required packages (e.g., transcription tools like `ffmpeg` or python audio libraries) using `sudo apt-get` or `pip` to decode the audio file.