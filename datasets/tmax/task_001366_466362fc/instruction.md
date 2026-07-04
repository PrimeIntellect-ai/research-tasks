You are tasked with fixing a critical security regression that has been bisected across 200 commits in our processing pipeline. A recent commit introduced an algorithmic vulnerability that causes a complete system crash and memory corruption when a specific payload is processed. 

The developer who bisected the issue left an audio report detailing the root cause analysis, but their workstation crashed before they could write the patch. We have recovered two key artifacts from the crashed container:
1. `/app/bisect_report.wav` - The developer's audio report.
2. `/app/pipeline.db-wal` and `/app/pipeline.db` - The corrupted SQLite database and its Write-Ahead Log (WAL) from the moment of the crash.

Your tasks:
1. Process the audio file `/app/bisect_report.wav` to understand the nature of the regression and how to identify the crashing payload.
2. Analyze the database WAL file (`/app/pipeline.db-wal`) to recover the exact malicious payload that caused the crash. The database schema has a table `logs(id INTEGER PRIMARY KEY, message TEXT)`.
3. Based on your findings, write a Python script at `/home/user/detector.py` that acts as a pre-filter to detect and block this payload type.

The script `/home/user/detector.py` must take a single file path as a command-line argument. It should read the contents of the file and:
- Print `REJECT` to stdout and exit with status code `1` if the file contains the malicious pattern (evil).
- Print `ACCEPT` to stdout and exit with status code `0` if the file is safe (clean).

We will verify your script against our hidden integration test suite, containing a corpus of known malicious payloads and clean logs.