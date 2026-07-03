You need to fix a configuration synchronization pipeline. We have a configuration data emitter running on `127.0.0.1:9001` and a receiver expecting processed data on `127.0.0.1:9002`. Currently, the data flow is broken because the intermediary data transformer is missing.

Your task is to write a purely Bash-based (utilizing standard tools like `awk`, `sed`, `tr`, etc., but no Python, Perl, or Ruby) stream processing script at `/home/user/mapper.sh` and then connect the services.

**Data Format & Transformation Rules:**
The emitter on port 9001 sends a stream of newline-separated configuration metric records. 
Format: `ID=<int> VALUE=<int> OP=<unicode_escaped_char> IP=<ipv4_address>`
Example: `ID=5 VALUE=10 OP=\u002B IP=192.168.1.50`

Your script `/home/user/mapper.sh` must read these lines from standard input and write the transformed data to standard output, adhering strictly to these requirements:
1. **Data Masking:** Anonymize the `IP` field by replacing the last two octets with `X.X` (e.g., `192.168.1.50` becomes `192.168.X.X`).
2. **Decoding:** The `OP` field contains a unicode-escaped mathematical operator. You must handle exactly three possible values: `\u002B` (which represents `+`), `\u002D` (which represents `-`), and `\u002A` (which represents `*`).
3. **Mathematical Evaluation:** Compute a `LOCAL_RESULT` by applying the unescaped operator to the VALUE and ID. 
   Calculation: `LOCAL_RESULT = VALUE [OP] ID`. (For the example above: `10 + 5 = 15`).
4. **Windowed Aggregation:** Maintain a rolling sum of the `LOCAL_RESULT` for the last 3 processed records. If fewer than 3 records have been processed, the rolling sum should just be the sum of the records seen so far.
5. **Output Format:** Output a single line per input record formatted exactly as:
   `[<MASKED_IP>] ROLLING_SUM=<sum>`
   Example Output: `[192.168.X.X] ROLLING_SUM=15`

**Service Composition:**
Once your script is ready and made executable, you must glue the services together so the pipeline runs in the background. Execute the pipeline exactly like this, logging any errors:
`nohup bash -c 'nc 127.0.0.1 9001 | /home/user/mapper.sh | nc 127.0.0.1 9002' > /home/user/pipeline.log 2>&1 &`

The automated system will independently test `/home/user/mapper.sh` with thousands of randomized inputs to ensure bit-exact equivalence to our reference parser, and it will also exercise the end-to-end `9001 -> script -> 9002` network flow.