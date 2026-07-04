I need you to build a reliable ETL pipeline for processing spoken telemetry logs. We have an audio recording of a technician dictating sensor readings over time, but the dictation includes accidental repetitions and is in a "wide" format (stating multiple sensors per timestamp).

First, you need to transcribe the audio file located at `/app/telemetry_log.wav`. You can use any available tool (like `ffmpeg` or `whisper` if installed, or whatever method you prefer) to recover the text. The spoken logs follow a pattern like: "Timestamp 1620000000. Sensor Alpha 45 point 2. Sensor Beta 12 point 0."

Second, I need a C++ program that performs the data transformation on this kind of telemetry data. The program must be saved as `/home/user/process_telemetry.cpp` and compiled to `/home/user/process_telemetry`.

The C++ program must read from standard input and write to standard output.
Input format (CSV, headerless):
`Timestamp,SensorAlpha,SensorBeta,SensorGamma`
Example:
`1620000000,45.2,12.0,9.1`

The C++ program must do the following:
1. **Validation & Logging**: Discard any lines that do not have exactly 4 columns or where the timestamp is not a valid integer. Log a warning to `stderr` for discarded lines: `WARNING: Invalid line`.
2. **Hash-based Deduplication**: Deduplicate rows. If a row has the exact same content as a previously seen row (matching all 4 columns exactly as strings), discard it. You must use a hash-set for this deduplication.
3. **Wide-to-Long Reshaping**: For each valid, unique row, output three lines to `stdout` in long format: `Timestamp,SensorName,Value`.
The sensor names should be output exactly as `SensorAlpha`, `SensorBeta`, and `SensorGamma`.

Example output for the input above:
```
1620000000,SensorAlpha,45.2
1620000000,SensorBeta,12.0
1620000000,SensorGamma,9.1
```

Finally, use your compiled C++ program to process the data you transcribed from the audio file (manually format the transcription into the CSV format first) and save the result to `/home/user/final_telemetry.csv`.

Ensure your C++ program strictly follows the IO requirements, as it will be rigorously tested against an automated fuzzer with random CSV inputs to ensure rock-solid reliability in our pipeline DAG.