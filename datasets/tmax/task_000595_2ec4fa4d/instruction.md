You are a capacity planner for a legacy system that exports its daily average CPU load telemetry via audio signals (to bypass a restricted network). 

You have been provided an audio file at `/app/telemetry.wav`. This file contains a sequence of 30 audio beeps separated by silence. Each beep represents the daily CPU load for a single day over a 30-day month.
The CPU load percentage for a given day is calculated directly from the duration of the beep:
`Load (%) = Duration of beep in milliseconds / 10`
For example, a beep lasting 450ms represents a 45.0% CPU load.

Your task is to automate the extraction and management of this capacity data:

1. **Audio Decoding Script**: Write a Python script at `/home/user/workspace/decode.py` that reads `/app/telemetry.wav`, identifies the duration of each beep (periods of audio where the amplitude is significantly above zero), calculates the CPU load percentage, and writes the results to `/home/user/workspace/loads.csv`. 
   - The CSV should have two columns: `Day` (1 to 30) and `Load` (float, rounded to 1 decimal place).

2. **Git Repository & Hook**: 
   - Initialize a Git repository in `/home/user/workspace`.
   - Create a `pre-commit` hook in this repository that reads `loads.csv` and REJECTS the commit (exits with a non-zero status) if any daily load is exactly 100.0% or greater.
   - Commit `decode.py` and `loads.csv` to the repository.

3. **Scheduled Task**:
   - Configure a user-level cron job that runs `/home/user/workspace/decode.py` every day at 02:00 AM.

Ensure your Python script relies only on standard libraries or commonly available packages like `numpy` or `scipy`.