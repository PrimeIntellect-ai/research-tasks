You are an operations engineer triaging an incident affecting our financial processing pipeline. Several issues have been reported:

1. **Network Payload Extraction**: A microservice has been crashing due to a malformed payload. We have captured network traffic in `/home/user/traffic.pcap`. Extract the corrupted JSON payload (the HTTP POST body that is missing closing braces/brackets or is otherwise malformed) and save exactly the raw body text into `/home/user/corrupted_payload.json`.

2. **Corrupted Input Handling**: The script `/home/user/process_tx.py` currently crashes when it encounters corrupted JSON data. Modify `process_tx.py` so that instead of crashing, it catches the parsing error, prints `Error: Corrupted input`, and continues processing any remaining lines.

3. **Floating-point Precision Repair**: An auditing service written in C (`/home/user/summarize.c`) computes the sum of transaction amounts from `/home/user/amounts.csv`. Due to floating-point precision loss with large numbers, it produces an incorrect total. Fix `summarize.c` by upgrading the relevant variables to use double precision (`double`), recompile it to `/home/user/summarize`, run it, and save the standard output to `/home/user/summary_result.txt`.

Ensure all tasks are completed in the `/home/user` directory. You may use any terminal tools you need (like `tshark`, `tcpdump`, standard compilers, etc.).