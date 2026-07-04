You are a data scientist cleaning up an ETL pipeline that handles incoming sensor telemetry. Due to network instability, the ingestion system occasionally retries failed requests. This results in "retry duplicates"—records that represent the same event but have slightly different timestamps and payload noise (due to random serialization artifacts).

Your task is to write a Bash script `/home/user/dedup_stream.sh` that acts as a streaming filter to sanitize datasets.

### Requirements

1. **Input / Output:**
   * Your script must read a CSV from `stdin` and write the cleaned CSV to `stdout`.
   * The CSV has three columns: `DeviceID,Timestamp,Payload`
   * The first line is always the header and must be emitted unchanged.

2. **Data Formats:**
   * `DeviceID`: Alphanumeric string.
   * `Timestamp`: Either an ISO-8601 string (e.g., `2023-10-25T14:30:00Z`) or a Unix epoch integer (e.g., `1698244200`). You must parse and align these to accurately compare times.
   * `Payload`: Base64-like encoded string.

3. **Retry Duplicate Logic:**
   * You must track the *most recently emitted* record for each `DeviceID`.
   * A new incoming row is considered a "retry duplicate" (and MUST be dropped) if ALL of the following conditions are met when compared to the most recently emitted record for the same `DeviceID`:
     a) The absolute time difference between the two timestamps is **<= 10 seconds**.
     b) The similarity score between the two `Payload` strings is **>= 0.85**.
   * If a row is dropped, it does NOT update the "most recently emitted" state for that `DeviceID`.
   * If a row is kept, it is emitted to `stdout` (exactly as it appeared in the input, preserving its original timestamp format) and becomes the new "most recently emitted" record for that `DeviceID`.

4. **Similarity Oracle:**
   * A pre-compiled utility is available at `/app/calc_sim`.
   * Usage: `/app/calc_sim "<string1>" "<string2>"`
   * It outputs a float between `0.0` and `1.0` to standard output. Use this to check the payload similarity.

Write your script using strictly Bash, coreutils, and standard CLI tools (`awk`, `sed`, `date`, etc.). You must handle the stateful tracking of DeviceIDs efficiently. Make sure your script is executable.