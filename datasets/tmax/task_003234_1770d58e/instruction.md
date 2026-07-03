You are a performance engineer tasked with profiling and debugging a data processing pipeline. 

You have a Python script located at `/home/user/process.py` that reads network packets from a capture file (`/home/user/traffic.pcap`), extracts JSON payloads from the TCP streams, and computes a mathematical metric (using an iterative Newton's method) for each extracted value. The script aggregates these metrics and writes the total to a file.

However, the pipeline is currently failing. When you run `python3 /home/user/process.py`, the script intermittently hangs and consumes 100% CPU without ever finishing. 

Your task is to debug and fix `/home/user/process.py` to satisfy the following requirements:
1. Identify and resolve the encoding/serialization issue: Some TCP payloads in the pcap file are not standard UTF-8. You must modify the script to correctly decode payloads whether they are UTF-8 or UTF-16LE.
2. Fix the convergence failure: The iterative function `compute_metric` can enter an infinite loop (convergence failure) if fed unexpected values (like negative numbers). Modify `compute_metric` so that it uses a maximum of 100 iterations. If it does not converge within 100 iterations (i.e., the loop condition is still true), it should return `0.0`.
3. After applying your fixes, run the script. It should successfully process the pcap file and write the final aggregated total to `/home/user/result.txt` formatted to two decimal places.

Do not remove the iterative Newton's method logic; just constrain it and fix the data ingestion.