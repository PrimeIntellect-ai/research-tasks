You are an IT Support Technician resolving an escalated ticket. 

A critical voice-mail ticket has been dropped into your queue. The audio file is located at `/app/ticket_recording.wav`. You will need to transcribe or listen to this audio file (you may install tools like `SpeechRecognition` or `whisper` via pip) to understand the exact nature of the user's issue. 

The user is complaining about a broken Python script: `/home/user/telemetry_parser.py`. This script is supposed to parse incoming hardware telemetry data from standard input, but it is currently failing. According to the crash logs (available at `/home/user/crash_trace.log`), the script frequently hits a recursion limit and crashes. 

Your objective is to debug and fix `/home/user/telemetry_parser.py` so that it perfectly matches the behavior of the legacy compiled parser, which is provided to you as a reference oracle at `/app/oracle_parser`.

The telemetry data format generally consists of lines like:
`[TIMESTAMP] DEVICE_ID: VOLTAGE | STATUS`
Example:
`[1634567890.123456] SENSOR_A: 12.045612 | OK`

The current Python script has multiple bugs:
1. It crashes or infinite-loops on corrupted input lines instead of recovering.
2. It loses floating-point precision on the voltage readings.
3. It has edge-case format parsing errors when trailing spaces or empty status codes are present.
4. It uses a recursive parsing function that fails catastrophically (core dump / stack trace provided) on large blocks of corrupted data.

Your task is to fix `/home/user/telemetry_parser.py`.
- It must read telemetry lines from `stdin`.
- It must output the exact same parsed JSON-line output to `stdout` as `/app/oracle_parser` does for *any* given input.
- It must handle corrupted input precisely as the oracle does (the oracle outputs `{"error": "corrupted_frame"}` for invalid lines and continues to the next line).
- You can test your script locally by running `echo "..." | python3 /home/user/telemetry_parser.py` and comparing it against `echo "..." | /app/oracle_parser`.

Ensure your final script is saved at `/home/user/telemetry_parser.py`. Our automated systems will verify your fix by running a fuzzing campaign, sending thousands of random, corrupted, and edge-case inputs to both your script and the oracle, verifying bit-exact stdout equivalence.