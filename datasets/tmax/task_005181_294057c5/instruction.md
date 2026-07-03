I need your help investigating some patterns in our chat logs, but the parsing rules were left as a voice memo by the previous log analyst. 

There is an audio file located at `/app/voice_memo.wav`. Please transcribe it to understand the anomaly detection and feature extraction rules for our text logs. 

Once you have the rules, write a Python script at `/home/user/log_analyzer.py` that implements them. The script must:
1. Read UTF-8 encoded text lines from standard input (`stdin`).
2. Implement the changepoint/anomaly detection logic exactly as described in the audio file.
3. Output the anomalous lines exactly as they are to standard output (`stdout`).

Make sure your Python script is executable and processes input robustly, as it will be tested against millions of log lines containing various Unicode characters and multiple languages.