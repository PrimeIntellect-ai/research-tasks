Hey, our CI build is failing on the data ingestion step, and we need your help to debug and fix it. 

The build runs a script located at `/home/user/build/ingest.py`. This script reads microservice logs from `/home/user/build/logs/`, reconstructs a unified timeline by parsing and sorting custom timestamps, and outputs a merged timeline. Recently, one of the microservices started emitting timestamps that occasionally trigger a parsing edge case, crashing the script.

Your tasks:
1. Identify the edge-case bug in the custom timestamp parsing logic. You are encouraged to write a short fuzzer script to feed random variants of the `YYYY-MM-DDTHH:MM:SS.mmmmmmZ` format into `parse_timestamp()` until it breaks, to confirm your diagnosis.
2. Repair `ingest.py` so that it safely parses the edge-case timestamps without losing chronological integrity (assume missing fractional seconds mean exactly `0` microseconds).
3. Run the repaired script to process the logs:
   `python3 /home/user/build/ingest.py /home/user/build/logs /home/user/build/merged_timeline.json`

The final output must be successfully written to `/home/user/build/merged_timeline.json` containing the reconstructed timeline as a valid JSON array of objects, sorted chronologically. Do not change the overall JSON structure or the keys (`service`, `timestamp`, `message`), only fix the parsing and ensure the script completes.