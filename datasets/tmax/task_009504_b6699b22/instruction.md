You are an operations engineer triaging a critical incident in our data processing pipeline. A background daemon process has hung, causing a build failure. We need to recover its lost configuration and identify the malformed network payload that caused the crash.

Here is what we know:
1. The daemon process (a Python script named `daemon_proc.py`) is currently running and hung.
2. The daemon reads its configuration from `/home/user/config.json` on startup, but a buggy cleanup script accidentally deleted this file from the filesystem. The running process still holds an open file descriptor to it.
3. Right before it hung, the daemon received a single UDP packet on port 9999. We captured this packet in `/home/user/traffic.pcap`.
4. The daemon expects UTF-8 encoded JSON payloads, but the system logs suggest an encoding/serialization mismatch occurred with the received payload.

Your task:
1. Recover the exact contents of the deleted `config.json` file from the hung process.
2. Extract the raw UDP payload from `/home/user/traffic.pcap` and decode it to a readable string (figure out what encoding was mistakenly used).
3. Create a JSON report at `/home/user/resolution.json` with the following exact structure:
```json
{
  "recovered_config": {
    "key1": "value1"
  },
  "decoded_payload": "the_decoded_string_value_here"
}
```

Ensure the `"recovered_config"` value is parsed as a JSON object, and `"decoded_payload"` is a string. Do not kill the hung process. All work should be done in `/home/user`.