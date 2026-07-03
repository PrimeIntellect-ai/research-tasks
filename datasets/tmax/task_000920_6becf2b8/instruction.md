You are a data analyst working on an automated telemetry pipeline. We have a set of raw sensor readings in `/home/user/sensor_data.csv`. The file has two columns: `timestamp` (integer) and `reading` (float). Some of the `reading` values are missing (empty strings).

We also received an audio file from the field operator at `/app/field_notes.wav`. This audio recording contains a short spoken phrase that provides two critical pieces of information:
1. An authentication passphrase.
2. A numeric calibration multiplier.

Your task is to build a complete processing and serving pipeline:

1. **Process the Audio:** Extract the authentication passphrase and the calibration multiplier from `/app/field_notes.wav`.
2. **Transform the Data:**
   - Read `/home/user/sensor_data.csv`.
   - Impute any missing `reading` values using linear interpolation based on the timestamp.
   - Multiply all `reading` values (both existing and imputed) by the calibration multiplier extracted from the audio.
   - Add a new column called `rolling_avg` which calculates a 3-period rolling average of the calibrated readings (use a window size of 3, minimum periods = 1).
3. **Database Import:** Bulk load this processed data into a new SQLite database at `/home/user/telemetry.db` in a table named `processed_data`.
4. **Data Serving:** Create and start an HTTP web service listening on `127.0.0.1:8000`. 
   - The service must expose an endpoint `GET /data?timestamp=<ts>`.
   - The endpoint must return JSON in the format: `{"timestamp": <ts>, "calibrated_reading": <val>, "rolling_avg": <val>}`.
   - The endpoint MUST be protected by Bearer token authentication. The required token is exactly the authentication passphrase spoken in the audio file.
5. **Pipeline Scheduling:** Create a shell script at `/home/user/export_db.sh` that dumps the SQLite database to `/home/user/backup.sql`. Configure the `user`'s crontab to execute this script automatically every 15 minutes.

Make sure your HTTP service is running in the background before you finish.