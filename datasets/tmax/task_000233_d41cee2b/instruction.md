You are an automation specialist for a remote monitoring facility. We receive daily telemetry reports via automated radio transmissions, which are recorded as audio files. Your task is to build an automated multi-stage ETL pipeline to process these audio logs into clean, aggregated data.

Here is your assignment:

1. **Transcription & Extraction**: 
   An audio recording of the latest telemetry transmission is located at `/app/telemetry_data.wav`. You need to transcribe this audio file. The audio contains spoken data points in the format: "Time X, Alpha Y, Beta Z", where X is a timestamp (in seconds: 0, 10, 20, up to 60), and Y and Z are numeric sensor readings. Some readings may be explicitly spoken as "missing" or omitted.

2. **Reshaping**: 
   Parse the transcribed text and convert the wide-format readings (Time, Alpha, Beta) into a strictly long-format dataset. Save this intermediate dataset as `/home/user/parsed_telemetry.csv` with exactly three columns: `time`, `sensor`, and `value`. For missing values, leave the `value` field blank (or standard null/NaN representation).

3. **Interpolation & Imputation**: 
   Read the long-format dataset. For any missing `Alpha` or `Beta` values at a given time step (time steps are strictly 0, 10, 20, 30, 40, 50, 60), perform linear interpolation based on the adjacent time steps to fill in the gaps. 
   Save the fully imputed long-format dataset to `/home/user/imputed_telemetry.csv`. The format must be exactly `time,sensor,value`.

4. **Aggregation**:
   Calculate the overall mean of the imputed values for the `Alpha` sensor and the `Beta` sensor. Save these summary statistics to a JSON file at `/home/user/summary.json` with the structure:
   ```json
   {
     "Alpha": {"mean": <float>},
     "Beta": {"mean": <float>}
   }
   ```

You may use any programming language, shell utilities, or open-source transcription tools (like whisper or ffmpeg) available or installable in the environment to orchestrate this pipeline. The automated verifier will strictly evaluate the numeric accuracy of your imputed dataset.