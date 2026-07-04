You are a security researcher analyzing an APT's data exfiltration mechanism. You have intercepted a stripped Linux binary used by the attackers, located at `/app/exfil_decoder`. 

You also managed to clone a partial Git repository left on a compromised staging server at `/home/user/apt_tool_repo`. The repository contains early development scripts for the exfiltration tool, but the attackers scrubbed the hardcoded 32-character hex initialization vector (IV) from the current `HEAD`.

Additionally, you have a directory of intercepted exfiltration logs at `/home/user/intercepted_traffic/`. These logs are fragmented. Each file contains a timeline of events, but the attackers intentionally corrupted the payloads:
1. The payloads are Base64 encoded, but the padding (`=`) has been stripped, and some non-standard URL-safe characters were mixed in (e.g., `-` instead of `+`, `_` instead of `/`).
2. The timestamps in the logs are recorded with floating-point precision (e.g., `1684321000.123456789`), but the binary strictly requires exactly 3 decimal places of precision (milliseconds) without rounding up (strict truncation). Passing the raw high-precision timestamps causes the binary's internal timeline state to corrupt, resulting in garbled output.

Your task:
1. Conduct forensics on `/home/user/apt_tool_repo` to recover the original 32-character hex IV.
2. Write a pure Bash script at `/home/user/analyze.sh` that:
   - Reads all `.log` files in `/home/user/intercepted_traffic/` (which have the format `TIMESTAMP|SOURCE_IP|CORRUPTED_PAYLOAD`).
   - Fixes the Base64 encoding issues (restoring standard characters and adding the correct padding).
   - Truncates the timestamps to exactly 3 decimal places (preventing precision loss/overflow in the binary).
   - Reconstructs the timeline sequentially by sorting the parsed events by the fixed timestamp.
   - For each event, invokes the binary to decode the payload: `/app/exfil_decoder --iv <RECOVERED_IV> --timestamp <FIXED_TIMESTAMP> --ip <SOURCE_IP> --payload <FIXED_BASE64>`
3. The binary will output a JSON object to standard output for successfully decoded payloads. Your `analyze.sh` script must collect all these JSON objects and append them to `/home/user/decoded_payloads.jsonl`.

The `analyze.sh` script should be executable (`chmod +x`). 

Ensure your final `decoded_payloads.jsonl` contains exactly one JSON object per line. An automated system will evaluate the extraction accuracy by comparing your JSONL output against the known ground-truth dataset.