You are an operations data engineer tasked with building a robust bash-based ETL pipeline. We receive sensor readings continuously in CSV format, but our upstream providers frequently send malformed files. Your goal is to build a validation checkpoint, apply a sampling and bucketing strategy, and schedule the pipeline.

**Step 1: The Validator**
We have a set of training data for you to test your logic. 
You must write a shell script at `/home/user/validate.sh` that takes a single file path as an argument. 
- It must exit with code `0` if the CSV is "clean" (perfectly formed, exactly 4 columns: `timestamp,sensor_id,value,status`).
- It must exit with code `1` (or any non-zero) if the CSV is "evil". Evil files contain anomalies such as embedded unescaped newlines that break standard line-by-line processing, or incorrect column counts. 
You can find test files to develop your script in `/app/corpus/clean/` and `/app/corpus/evil/`. Your script must perfectly separate clean and evil files.

**Step 2: The Bucketing Rules**
We have received a dictation from the lead architect regarding how the clean data should be bucketed and sampled. The audio file is located at `/app/audio_rule.wav`. 
Extract the spoken instruction from this audio file (hint: the transcription has also been embedded in the file's metadata for programmatic access if you lack audio processing tools). 
Write a script at `/home/user/process.sh` that reads a clean CSV, applies the time-based bucketing and data sampling rule dictated in the audio, and outputs the resulting data to stdout.

**Step 3: Scheduling**
Create a script `/home/user/setup_cron.sh` that, when run, installs a crontab entry for the user `user` to execute `/home/user/pipeline.sh` at minute 0 past every 4th hour (e.g., 00:00, 04:00, 08:00...). 

Ensure all scripts are executable.