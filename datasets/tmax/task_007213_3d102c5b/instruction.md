You are tasked with recovering system configuration files that were corrupted due to a race condition in a custom log rotation script. 

The broken backup system dumped configuration states into `/home/user/raw_configs`. These files have a `.cfl` (Custom Filtered Log) extension. You need to write a Bash script (save it anywhere, but you must execute it to produce the final output) to parse, clean, and consolidate these files.

Here is the exact structure of every `.cfl` file:
1. **Line 1 (Metadata):** A plaintext header in the format `METADATA - HOST:<hostname> DATE:<epoch_timestamp>`. For example: `METADATA - HOST:web-01 DATE:1680001000`
2. **Line 2 to EOF:** A Base64-encoded, Gzip-compressed configuration file.

Due to the race condition, the extracted text files contain corrupted injected lines. Every line in the extracted configuration that begins EXACTLY with the string `[DIRTY_WRITE_FLAG]` is a corruption artifact and must be completely removed.

Your objective is to:
1. Find all `.cfl` files in `/home/user/raw_configs` (and its subdirectories).
2. Read the metadata to determine the host and the timestamp.
3. Decode the Base64 payload and decompress it using gzip to get the raw config text.
4. Remove all lines starting with `[DIRTY_WRITE_FLAG]` from the extracted text.
5. For each unique host, identify the configuration with the **highest** (latest) epoch timestamp.
6. Assemble the cleaned configurations of the latest files into a single valid JSON file located at `/home/user/clean_state.json`.

The final `/home/user/clean_state.json` must be a single JSON object where the keys are the hostnames, and the values are the corresponding cleaned, multi-line configuration text.

Example expected structure for `/home/user/clean_state.json`:
```json
{
  "web-01": "listen=80\nmax_clients=100\n",
  "db-main": "port=3306\n"
}
```

Ensure all dependencies you might need (like `jq`, `base64`, `gzip`) are used correctly via Bash commands. Generate the final `/home/user/clean_state.json` file to complete the task.