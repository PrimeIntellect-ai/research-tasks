You are a Database Reliability Engineer (DBRE) managing a critical SQL backup pipeline. We recently detected unauthorized data exfiltration attempts embedded within our daily backup query logs. The attacker is trying to extract data from a highly sensitive table by hiding subqueries and joins inside otherwise normal-looking analytical queries.

The incident response team left an automated voice memo regarding the breach at `/app/voicemail.wav`. 

Your objectives are:
1. Process the audio file `/app/voicemail.wav` to discover the exact name of the compromised, highly sensitive table. (You may use tools like `ffmpeg` and `whisper` if installed, or install them, to transcribe the audio).
2. Write a strict Bash sanitization script at `/home/user/filter_backup.sh`. 
3. The script must accept a single argument: the path to a `.sql` file containing a query from the backup logs.
4. The script must analyze the SQL file (using tools like `awk`, `grep`, `sed`, etc.) to determine if it queries or references the sensitive table mentioned in the audio. Note that the table name might appear in `FROM` clauses, `JOIN`s, subqueries, or CTEs, and might be surrounded by quotes or backticks.
5. If the file is benign (does NOT reference the sensitive table), your script must exit with status code `0` and print `CLEAN` to stdout.
6. If the file is malicious (references the sensitive table), your script must exit with status code `1` and print `EVIL` to stdout.

We have provided a sample dataset to test your script:
- `/app/corpus/clean/`: Contains known good backup queries.
- `/app/corpus/evil/`: Contains known malicious queries targeting the sensitive table.

Your script `/home/user/filter_backup.sh` must be executable and will be tested automatically against a hidden evaluation suite of clean and evil queries using the exact same table criteria. To pass, it must correctly classify 100% of the clean corpus as safe and 100% of the evil corpus as malicious.