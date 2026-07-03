You are tasked with building a streaming ETL pipeline in Python that processes time-series sensor telemetry, performs stateful imputation, and handles multi-language/unicode text.

First, you need to determine the exact output format required for the pipeline. The requirements were recorded in an audio voice memo by the lead engineer. 
1. Transcribe the audio file located at `/app/memo.wav`. You may use any available command-line tool (like `whisper` if you install it, or any other transcription utility) to listen to or transcribe the file.
2. The memo dictates the exact text template you must use for formatting each processed record.

Next, create the ETL pipeline script at `/home/user/etl.py`. The script must satisfy the following strict specifications:
- **Input**: It must read a continuous stream of JSON Lines (JSONL) from standard input (`sys.stdin`). You must stream the file line-by-line (do not load the entire input into memory, as it may be very large).
- **Data Structure**: Each JSON object will have the following keys:
  - `ts` (integer): The timestamp of the reading.
  - `sensor` (string): The identifier of the sensor.
  - `temp` (float or null): The temperature reading. May be missing (`null`).
  - `status` (string): A unicode string representing the sensor's multi-language status (e.g., "正常", "⚠️ Error", "Activo").
- **Imputation Logic**: Time-series sensors frequently drop temperature readings. You must perform forward-fill imputation independently for each `sensor`. 
  - If `temp` is `null`, replace it with the last known valid `temp` for that specific `sensor`.
  - If a sensor's `temp` is `null` and it has no prior valid readings in the stream, use a default value of `0.0`.
- **Output**: For every input line, print exactly one line to standard output (`sys.stdout`). The line must be formatted using the template described in the audio memo `/app/memo.wav`. Make sure to append a space and the `status` unicode string to the very end of the template instructed in the audio.

Your script must perfectly match the behavior of our reference implementation. Ensure edge cases like consecutive `null` values for a sensor are handled correctly according to the forward-fill rule.

Please write the complete Python script to `/home/user/etl.py`.