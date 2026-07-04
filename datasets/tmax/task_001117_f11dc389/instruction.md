You are an on-call engineer, and you've just been paged at 3 AM. The audio monitoring pipeline for our server room alert system is failing. 

The pipeline uses a Bash script located at `/app/process_alert.sh` to analyze audio files. It extracts the RMS volume level of each audio frame using `ffmpeg` and calculates a 5-period Simple Moving Average (SMA) of these levels to smooth out transient noise. 

However, the script is crashing and producing incorrect results for a new alert recording: `/app/alert_log.wav`.

Your investigation reveals three issues:
1. **Format parsing edge-case**: The audio file contains segments of absolute silence. For these segments, `ffmpeg` outputs `-inf` for the RMS level. The script attempts to pass `-inf` directly into `bc` for arithmetic, causing a fatal syntax error. 
2. **Formula implementation correction**: The moving average logic in the Bash script is flawed. For the first 4 frames (before a full window of 5 is available), it incorrectly divides the sum by 5 instead of the actual number of available frames (1, 2, 3, and 4 respectively).
3. **Delta debugging**: You need to run the script and isolate the exact frames causing the failure, then apply the fixes.

Your task is to fix `/app/process_alert.sh` so that it successfully processes `/app/alert_log.wav`.
- You must modify the script to replace any `-inf` values with `-100.0` before performing calculations.
- You must fix the moving average calculation so that it dynamically divides by the correct window size (min(current_count, 5)).
- The script should write the corrected sequence of moving averages (one number per line) to `/home/user/smoothed_levels.txt`.

Ensure your corrected script executes successfully and writes the required output. Do not change the input file path in the script, it should still process `/app/alert_log.wav`.