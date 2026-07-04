You are a performance engineer tasked with debugging and optimizing a legacy data processing pipeline for audio analysis. 

We have an audio analyzer script located at `/app/audio_analyzer.sh` that processes a 5-minute recording `/app/test_audio.wav`. The script is supposed to:
1. Extract the absolute amplitude envelope of the audio at a 100Hz sample rate.
2. Apply a 10-point moving average to smooth the envelope.
3. Compute the global mean and standard deviation of this smoothed envelope.
4. Output the timestamps (in seconds) of "statistical anomalies" — defined strictly as instances where the smoothed amplitude is strictly greater than `GlobalMean + 3 * GlobalStdDev`.

Currently, the script is a disaster:
- **Crash/Recursion:** It often crashes with a stack trace indicating deep recursion or a bash stack overflow because of a broken loop/recursion termination in the smoothing function.
- **Formula Error:** The statistical formulas implemented in the script for standard deviation are mathematically incorrect, leading to false anomalies.
- **Performance:** It runs incredibly slowly (spawning thousands of subshells or subprocesses) instead of effectively using standard pipelines (`awk`, `sed`, etc.).

Your task:
1. Diagnose and fix the recursion/loop termination bug so the script runs to completion.
2. Correct the mathematical formula for Standard Deviation. (Recall: Population StdDev = sqrt( sum((x - mean)^2) / N )).
3. Radically optimize the Bash/Awk script so that it finishes processing the audio file very quickly.
4. Ensure the output is a perfectly accurate list of anomaly timestamps.

Write your final, completely fixed, and optimized script to `/home/user/fixed_analyzer.sh`.
Your script must accept two arguments: 
`$1` = Input audio file path
`$2` = Output text file path

Run your script:
`/home/user/fixed_analyzer.sh /app/test_audio.wav /home/user/anomalies.txt`

The file `/home/user/anomalies.txt` must contain exactly one timestamp per line (formatted to 2 decimal places, e.g., `12.45`) where anomalies were detected. 

We will verify both the mathematical correctness of your outputs and the performance of your script. It must process the 5-minute audio in under 2 seconds.