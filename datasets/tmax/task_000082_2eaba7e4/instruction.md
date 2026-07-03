You are a localization engineer managing a time-series telemetry pipeline that tracks translation updates. We have a legacy stripped binary executable located at `/app/loc_masker` which processes JSONL streams of translation events. It performs critical data masking, Unicode normalization, and formatting.

Because the old binary is single-threaded and slow, your task is to reverse-engineer its behavior and rewrite it in Python so we can run it in parallel.

Here is what you need to do:

1. **Analyze the Oracle:** 
   Execute `/app/loc_masker`. It reads a JSONL stream from `stdin` and writes the processed JSONL to `stdout`. 
   The input format is:
   `{"timestamp": 1690000000, "locale": "es-ES", "original": "Contact support@example.com", "translated": "Contacte a support@example.com", "editor_ip": "192.168.10.45"}`
   Experiment with various inputs (including complex Unicode, different IPs, and emails) to determine exactly how it transforms the text and fields.

2. **Develop the Python Replacement:**
   Write a Python script at `/home/user/fast_masker.py` that reads JSONL from `stdin` and writes to `stdout`. It must produce **byte-for-byte identical output** to `/app/loc_masker` for any valid JSONL translation event. Ensure it handles Unicode gracefully.

3. **Parallel Processing & Cron:**
   Write a bash script `/home/user/parallel_process.sh` that takes a file path as an argument, splits the file into chunks, processes them in parallel using your Python script, and outputs the merged result to `stdout`. 
   Create a cron schedule file at `/home/user/loc_sync.cron` containing a valid cron expression to run `/home/user/parallel_process.sh /data/events.jsonl > /data/processed.jsonl` every day at 2:00 AM.

Focus heavily on getting `/home/user/fast_masker.py` to exactly mimic `/app/loc_masker`. Automated verification will blast thousands of random JSONL lines through both to ensure exact equivalence.