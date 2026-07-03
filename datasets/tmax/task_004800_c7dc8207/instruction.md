You have received a voicemail from the Lead Data Engineer regarding a new time-series pipeline for our sensor network. The audio file is located at `/app/voicemail.wav`.

Your task is to:
1. Extract the pipeline specifications from the audio file.
2. Implement a Python script at `/home/user/pipeline.py` that fulfills these requirements.

The script must:
- Read CSV data from `standard input` (`sys.stdin`).
- Write the processed data as a JSON array to `standard output` (`sys.stdout`).
- Strictly adhere to the parsing rules, windowed aggregation, normalization steps, and the specific data-cleaning edge case mentioned in the recording. 
- Use standard Python libraries.

The input CSVs will always have the following header:
`timestamp,sensor_id,temperature,status_log`

The evaluation system will feed thousands of randomly generated, complex CSV files to your script via `stdin` and compare the standard output against a golden reference implementation. Your script's output must be BIT-EXACT equivalent to the reference, so pay close attention to rounding rules and formatting specified in the audio.