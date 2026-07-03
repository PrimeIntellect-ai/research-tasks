You are an IT support technician helping a data scientist. They have submitted the following ticket:

"My background math worker script, `/home/user/sequence_worker.py`, has completely stalled. It calculates a recursive sequence, but it seems to have hung. Worse, I accidentally deleted the `/home/user/config_multiplier.txt` file, which contained a critical multiplier value required for the sequence calculations! Since the stalled script is still running in the background, I am hoping the file descriptor is still open and you can recover the value. The script also writes its intermediate execution state to `/home/user/sequence_trace.log`."

Your task is to resolve the ticket by performing the following actions:
1. Identify the running process for `sequence_worker.py` and recover the exact contents of the deleted `config_multiplier.txt` file using the `/proc` filesystem. Save the recovered contents to `/home/user/recovered_multiplier.txt`.
2. Inspect the intermediate states in `/home/user/sequence_trace.log` to determine the integer ID of the *last successfully completed* sequence (look for the highest sequence ID that has a matching "COMPLETED" entry).
3. Create a final ticket resolution report at `/home/user/ticket_resolution.txt`. This file must contain exactly two lines:
   - Line 1: The recovered multiplier value.
   - Line 2: The integer ID of the last completed sequence.

Kill the stalled background process once you have recovered the necessary information.