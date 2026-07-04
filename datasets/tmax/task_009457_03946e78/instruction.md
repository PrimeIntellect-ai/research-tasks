Wake up, it's 3:00 AM and PagerDuty is going off. 

The nightly telemetry processing pipeline has failed. This pipeline reads a daily packet capture of UDP telemetry data, parses the JSON payloads, and aggregates the results. The cron job that runs the build and execution script has crashed, and downstream dashboards are empty.

You need to investigate and fix the pipeline located in `/home/user/pipeline`.

Here is what we know:
1. The entry point is `/home/user/pipeline/build_and_run.sh`. It sets up dependencies and runs the data processor. Currently, it fails immediately.
2. The processing script is `process_telemetry.py`. It is supposed to read `/home/user/pipeline/telemetry.pcap` and write an output file.
3. A recent firmware update on some IoT sensors means that occasionally, a sensor sends a malformed binary diagnostic packet instead of the expected JSON payload on the UDP telemetry port (port 5000). The current Python code does not handle this gracefully and crashes.

Your objectives:
1. Diagnose and fix the build/dependency failure in `build_and_run.sh` / `requirements.txt`.
2. Debug and modify `process_telemetry.py` so that it successfully parses the PCAP file. 
3. When `process_telemetry.py` encounters a UDP packet on port 5000 with a payload that cannot be decoded as valid JSON, it must gracefully skip it, but it MUST record the source IP address of that specific malformed packet.
4. The script must create a file exactly at `/home/user/pipeline/bad_ips.txt` containing the source IP(s) of the malformed packet(s), one IP per line.
5. The script must successfully finish processing the remaining packets and write its normal output to `/home/user/pipeline/summary.json` containing the total count of valid JSON telemetry packets in this exact format: `{"valid_packets": <integer>}`.

You are finished when running `bash build_and_run.sh` completes with exit code 0, and both `bad_ips.txt` and `summary.json` contain the correct information based on the provided `telemetry.pcap`.