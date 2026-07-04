A severe system failure occurred last night. The main logging server went down, and the only remaining record of the real-time telemetry right before the crash is a screen recording captured by a KVM over IP system. Furthermore, a junior DevOps engineer accidentally deleted our log-parsing bash script from a backup disk image.

Your task is to recover the logs, fix our parsing pipeline, and generate a final summary report. 

Here are the specific steps you must take:

1. **Recover the Parser:** 
   You have been provided an ext4 filesystem image at `/app/backup.img`. A bash script named `parser.sh` was recently deleted from the root of this filesystem. Recover `parser.sh` to `/home/user/parser.sh`.

2. **Extract Telemetry from Video:**
   The KVM recording is located at `/app/crash_vid.mp4`. 
   Extract the log lines visible in this video. The logs format is `[TIMESTAMP] [LEVEL] METRIC=VALUE`.
   Save the raw extracted text into `/home/user/raw_logs.txt`. (You may use `ffmpeg` and `tesseract` or any other tools you prefer).

3. **Debug and Fix the Parser (Fuzzing & Convergence Repair):**
   The recovered `parser.sh` takes a log file as an argument and outputs a CSV summary to stdout. However, it is notoriously buggy. It hangs in infinite loops (convergence failure) when encountering malformed lines or specific edge cases. 
   Write a small bash fuzzer to feed it randomized or mutated log lines to identify its crashing/hanging inputs. Add intermediate assertion checks (`set -e`, custom validation functions) to the script and fix the logic so it can process noisy OCR outputs without hanging or crashing.

4. **Generate the Final Summary:**
   Run your fixed `parser.sh` on `/home/user/raw_logs.txt` and pipe the standard output to `/home/user/summary.csv`.
   The final CSV should have the headers: `Timestamp,Level,Metric,Value`.

Ensure `/home/user/summary.csv` is correctly populated. Your work will be evaluated based on the accuracy of this final CSV compared to the actual events in the video.