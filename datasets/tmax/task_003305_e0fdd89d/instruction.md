We are experiencing issues with our configuration manager. It tracks configuration changes across our server fleet and dumps them into JSON-lines (JSONL) logs. Unfortunately, a recent bug in the logging agent injected malformed data into the stream, causing standard JSON parsers like `jq` or Python's `json` module to crash or hang on specific complex unicode escape sequences.

We need you to process these logs using standard Bash text-processing tools to bypass the broken parsers. 

The logs are located in `/home/user/logs/` as multiple `.jsonl` files. 

Write a Bash script at `/home/user/process_configs.sh` that performs the following tasks:
1. **Parallel Processing**: Process all `.jsonl` files in `/home/user/logs/` in parallel.
2. **Streaming and Regex Extraction**: Stream the files and extract events where the `config_key` starts with the string `network.`. You must use text processing tools (like `grep`, `sed`, `awk`) to extract the `config_key` and `config_value` fields from the JSON lines.
    * Example line: `{"event": "update", "config_key": "network.proxy.url", "config_value": "http\u003a\u002f\u002fproxy.local\u003a8080", "timestamp": 1679921020}`
3. **Feature Transform**: The `config_value` fields contain unicode hex escape sequences (e.g., `\u003a` for `:`, `\u002f` for `/`, `\u003d` for `=`). You must decode these `\uXXXX` sequences back into their standard ASCII characters.
4. **Hash-based Deduplication**: Format each extracted and decoded pair as `key=value` (e.g., `network.proxy.url=http://proxy.local:8080`). Compute the MD5 hash of this exact string. 
5. **Output**: Deduplicate the results so each unique `key=value` pair only appears once. Write the final deduplicated list to `/home/user/unique_network_configs.txt`. Each line must be formatted as `<MD5_HASH>  <key>=<value>` (note the double space after the hash, typical of `md5sum` output). Sort the final output file alphabetically by the MD5 hash.

Constraints:
* Do NOT use `jq`, `python`, `perl`, `ruby`, or Node.js. Use only standard bash built-ins and coreutils (e.g., `grep`, `sed`, `awk`, `xargs`, `md5sum`, `sort`).
* The script must execute successfully when run as `bash /home/user/process_configs.sh`.