You are an IT support technician assigned to resolve a critical ticket regarding a transaction processing script. The script is occasionally producing incorrect checksums due to logical and concurrency errors, and it recently crashed, leaving behind a raw memory dump.

Your tasks are to:
1. Analyze the memory dump located at `/home/user/crash_memory.dump`. Within the garbage data, find the exact transaction payload that caused the crash. The payload is a comma-separated list of integers enclosed between the markers `PAYLOAD_START{` and `}PAYLOAD_END`.
2. Investigate and fix the script located at `/home/user/processor.py`. 
   - **Formula Implementation**: The `calc_hash` function contains an order of operations bug. The intended formula is to first add `0x5A` to the value, then multiply the sum by `13`, and finally take the modulo `256` of that entire result. Currently, it evaluates incorrectly.
   - **Concurrency Bug**: The script processes numbers across multiple threads and updates a global `total_checksum` variable. There is a race condition leading to lost updates. Introduce the necessary synchronization mechanism (e.g., a threading lock) to ensure the final `total_checksum` is correctly computed.
3. Run your fixed `/home/user/processor.py` script, passing ONLY the extracted comma-separated payload (the numbers between the braces, no spaces, no braces) as the first command-line argument.
4. Save the final output (just the resulting total checksum number) to a file named `/home/user/resolution.txt`.

Ensure your fixes in the Python code do not change the number of threads or the overall structure of the multithreading beyond fixing the race condition and the formula error.