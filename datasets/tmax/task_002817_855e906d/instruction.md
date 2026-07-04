We are in the process of porting our legacy log-processing pipeline into a minimal container environment. The old environment used heavy external dependencies, but the new minimal container needs to accomplish the same tasks using standard built-ins, coreutils, or a lightweight script.

You need to process a text file located at `/home/user/data/payloads.txt`. Each line in this file contains a semantic version number followed by a space and a hex-encoded string payload.

Your task is to:
1. Parse `/home/user/data/payloads.txt`.
2. Filter the entries based on semantic versioning constraints: you must ONLY keep entries where the version is strictly greater than or equal to `1.5.0`. Be careful to handle semantic versioning correctly (for example, `1.11.2` is greater than `1.5.0`).
3. Decode the hex-encoded string of the matching entries into standard ASCII text.
4. Construct a JSON array containing the filtered and decoded data. This JSON will act as the mock payload for our new REST API. Save this JSON file to `/home/user/api_response.json`.
   The JSON should be formatted exactly like this:
   ```json
   [
     {
       "version": "1.5.0",
       "data": "decoded string here"
     },
     ...
   ]
   ```
5. We need to evaluate the performance of your parsing approach. Run your entire processing pipeline (whether it is a bash command chain, `awk`, `python`, etc.) via a benchmarking command like `time`. Redirect or save the output of the benchmarking tool (e.g., the output showing real/user/sys times) into `/home/user/benchmark.txt`.

Ensure your final JSON file is valid. You have full shell access to complete this multi-step task.