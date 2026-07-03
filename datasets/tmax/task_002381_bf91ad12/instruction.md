You are a log analyst investigating a series of server intrusions. We have captured an audio recording of the attackers discussing their tools, and we have a corpus of log files—some of which contain their malicious traces.

Your task is to write a C++ data validation tool that can classify log files as either "clean" (normal traffic) or "evil" (containing malicious or malformed entries). 

1. **Audio Transcription**: 
   Listen to or transcribe the audio file located at `/app/intercept.wav`. In it, the attacker dictates their secret 4-digit `user_id` which they use as a backdoor account. 

2. **C++ Log Validator**:
   Create a C++ program at `/home/user/validator.cpp` and compile it to `/home/user/validator`. 
   The program must accept exactly one argument: the file path to a CSV log file.
   The CSV files have the following header: `event_id,timestamp,user_id,status,payload`

   Your program must parse the CSV and validate every row (ignoring the header). A file is considered "evil" (and your program must exit with status code `1`) if **ANY** row meets one or more of the following anomaly constraints:
   - `user_id` matches the 4-digit secret ID spoken in `/app/intercept.wav`.
   - `timestamp` is a negative integer or contains non-numeric characters.
   - `status` is not exactly one of these strings: `OK`, `WARN`, `ERR`.
   
   If all rows in the file are valid, the file is "clean", and your program must exit with status code `0`.

3. **Validation**:
   Your compiled binary `/home/user/validator` must correctly classify 100% of the files in the provided adversarial corpora:
   - Clean files are located in `/app/corpus/clean/` (all must yield exit code 0).
   - Evil files are located in `/app/corpus/evil/` (all must yield exit code 1).

You may use shell utilities (like `ffmpeg`, `python3` or download transcription tools) to extract the spoken ID from the WAV file. Ensure your C++ program is compiled and works perfectly on the provided corpora.