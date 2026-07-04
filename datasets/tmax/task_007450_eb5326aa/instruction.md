You are an operations engineer triaging a critical incident where a legacy data processing pipeline has suddenly crashed. The original Python parser script was accidentally deleted during the incident, and the encrypted event logs have been partially corrupted by a failing disk.

Your task is to perform forensic recovery to extract the critical failure event.

You have access to the following artifacts:
1. `/home/user/memdump.bin`: A raw memory dump from the server. The deleted Python parsing script is still present in this dump, bounded by the exact strings `# BEGIN PARSER` and `# END PARSER`.
2. `/home/user/auth_service`: A compiled binary that was running on the system. It contains a hardcoded legacy fallback key formatted as `SECRET_AUTH_KEY_<alphanumeric>`.
3. `/home/user/events.dat`: The corrupted event log file. It contains a payload that must be decrypted using the recovered Python script and the extracted key. However, the first few bytes of this file have been corrupted by the disk failure (containing non-ASCII junk bytes).

Your objective:
1. Recover the deleted Python script from `/home/user/memdump.bin` and save it to `/home/user/parser.py`.
2. Extract the secret key from the `/home/user/auth_service` binary.
3. The recovered Python script expects valid ASCII input. You will need to either clean the corrupted `/home/user/events.dat` to remove the non-ASCII junk bytes at the beginning, or modify `parser.py` to handle the corrupted input correctly.
4. Run the parser script using the cleaned input and the extracted key to decode the final event string.
5. Save the exact decoded string to `/home/user/recovered_event.txt`.