You are a security researcher investigating a suspicious data processing pipeline found on a compromised Linux system. 

You have been provided with the following files in `/home/user/`:
- `process_data.sh`: A Bash script that drives the data decoding pipeline.
- `decoder`: A stripped ELF executable called by the bash script.
- `raw_data.txt`: A file containing a stream of encoded payloads.

The `process_data.sh` script attempts to process the encoded payloads concurrently for speed, but it contains a severe race condition causing the final output to be corrupted, truncated, or interleaved. Additionally, the exact encoding/decoding mechanism inside the `decoder` binary is unknown, but it is suspected to use a hardcoded single-byte XOR key.

Your task is to:
1. Reverse engineer the `decoder` binary to identify the single-byte XOR key used to decode the data. Write this key in hexadecimal format (e.g., `0x1F`) to `/home/user/xor_key.txt`.
2. Debug and fix the race condition in `/home/user/process_data.sh`. The script MUST continue to process the data concurrently (using background jobs `&`), but it must safely gather all decoded outputs without data corruption or loss.
3. Modify the script so that the final aggregated output written to `/home/user/final_output.txt` has its lines sorted alphabetically.
4. Run the fixed `/home/user/process_data.sh` to successfully decode `/home/user/raw_data.txt` and produce the correct `/home/user/final_output.txt`.

Ensure your fixed script is robust and leaves no temporary files behind after successful execution.