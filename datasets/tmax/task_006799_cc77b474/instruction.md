You have recently inherited a legacy sensor data ingestion pipeline located in `/home/user/pipeline`. The pipeline is supposed to extract UDP payloads from a network capture file, aggregate the floating-point sensor readings, and save the final report. However, the pipeline is currently broken and failing to produce the correct output.

Your goal is to debug and fix the pipeline so that it successfully runs and generates the correct output file at `/home/user/pipeline/output/results.txt`.

Here is what you know about the system:
1. The entry point is `/home/user/pipeline/run.sh`. You should be able to run `bash /home/user/pipeline/run.sh` without any errors.
2. The pipeline relies on an environment configuration file `config.env`. There appears to be a misconfiguration in how the data directory is defined or loaded, which breaks the shell script because the target directory (`raw data`) contains a space.
3. The script processes a packet capture file (`sensor.pcap`). The Python script `aggregate.py` extracts JSON payloads from UDP packets (destination port 5000). 
4. The aggregation logic in `aggregate.py` suffers from floating-point precision issues. It sums pairs of values like `0.1` and `0.2`, but downstream systems strictly require the output to be exact (e.g., `0.3`, not `0.30000000000000004`). You must modify the code to ensure precise decimal arithmetic is used instead of standard IEEE 754 floats.

Requirements:
- Fix the environment variable and shell script quoting issues so the pipeline gracefully handles directories with spaces.
- Fix the floating-point logic in `aggregate.py`.
- Ensure that running `/home/user/pipeline/run.sh` produces `/home/user/pipeline/output/results.txt`.
- The `results.txt` file must contain one line per packet payload processed, structured as `Packet <N>: ExactSum`.

Make any necessary modifications to the files in `/home/user/pipeline/` to accomplish this.