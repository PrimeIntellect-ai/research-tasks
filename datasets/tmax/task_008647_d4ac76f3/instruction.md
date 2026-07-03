You have just inherited an unfamiliar legacy log-processing pipeline from a developer who recently left the company. The pipeline is located in `/home/user/pipeline/`.

You are told that the pipeline recently started hanging indefinitely when processing new batches of logs. 

The pipeline consists of:
1. `run.sh`: A shell script that acts as the orchestrator.
2. `parser.py`: A Python script that extracts tagged data from standard input.
3. `large_input.txt`: A recent batch of 5,000 log lines.

Your task is to perform forensics on this pipeline:
1. **Delta Debugging / Minimization:** Isolate the exact single line of log data in `large_input.txt` that is triggering the intermittent hang/infinite loop. Write this exact, full line to `/home/user/bug_report.txt` (just the line of text, no extra commentary).
2. **Loop Termination Fixing:** Identify the bug in `parser.py` that causes the infinite loop and modify the code to safely break out of the loop or skip the malformed segment without hanging. Malformed tags (missing a closing `</data>` tag) should simply be ignored, and the script should move on to the next line.
3. **Execution:** Once fixed, run the pipeline on the full `large_input.txt` and redirect the successful output to `/home/user/pipeline_output.txt`.

Requirements:
- Do not remove or skip valid data lines.
- `/home/user/bug_report.txt` must contain exactly the raw log line that caused the failure.
- `/home/user/pipeline_output.txt` must contain the correctly extracted data payloads, one per line.