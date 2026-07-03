You are a Site Reliability Engineer (SRE) responsible for the uptime monitoring pipeline. Our telemetry ingestion system recently crashed due to malformed mathematical anomalies in the probe data, and our specialized JSON processing tool is currently failing to build. 

Your task consists of three phases to restore the pipeline:

**Phase 1: Fix the Vendored Package**
We vendor a specific version of `jq` (version 1.6) for high-performance JSON log querying. A previous engineer attempted to optimize the build configuration but broke it. The source is located at `/app/jq-1.6`. 
When you run `make` in that directory, it fails during the linking stage with undefined mathematical references (like `pow`, `exp`, `atan2`). 
Diagnose the build failure, fix the `Makefile` or build configuration, and successfully compile the `jq` executable at `/app/jq-1.6/jq`.

**Phase 2: Binary Reverse Engineering**
The probes authenticate their payloads using a numeric token. You have been provided a compiled, stripped binary at `/usr/local/bin/token_validator` (which we no longer have the source code for). This binary takes two integer arguments: `probe_id` and `token`. It exits with status `0` if the token is mathematically valid for that probe, and `1` otherwise.
By analyzing this binary (using tools like `ltrace`, `strace`, `objdump`, or `gdb`), determine the mathematical formula used to validate the token based on the `probe_id`.

**Phase 3: Create the Adversarial Telemetry Filter**
Write a Python script at `/home/user/telemetry_filter.py` that reads a JSON payload from standard input. This script acts as a sanitization gatekeeper before data enters our time-series database.

The script must exit with status `0` (ACCEPT) if ALL of the following are true:
1. The JSON contains numeric fields: `probe_id`, `token`, `uptime_sec`, `total_sec`.
2. `total_sec` is strictly greater than 0.
3. `uptime_sec` is greater than or equal to 0, and mathematically cannot exceed `total_sec`.
4. The `token` is valid for the `probe_id` according to the formula you reverse-engineered in Phase 2.

The script must exit with status `1` (REJECT) if any condition is violated, or if the JSON is malformed/missing fields. 
*Note: Do not call the `token_validator` binary from your script; you must implement the reverse-engineered mathematical logic directly in Python to handle high throughput.*

You can test your script against the unverified telemetry corpora located at `/app/corpus/clean/` and `/app/corpus/evil/`. Your script must perfectly separate the valid telemetry from the mathematically impossible/malicious telemetry.