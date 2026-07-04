You are the on-call engineer, and you've just been paged at 3:00 AM. 

The "QuantAgg" service, which calculates risk metrics for our financial backend, has completely failed. The original developer is unreachable. 

Here is what we know:
1. The service was supposed to read a dataset from `/home/user/data/inputs.dat`. This file contains multiple binary records. Each record consists of a 4-byte unsigned integer (big-endian) representing the length of the following payload, followed by the payload itself. The payload is a UTF-16LE encoded JSON string of the format: `{"id": "A1", "values": [10.5, 12.1, ...]}`.
2. The old service attempted to calculate the **Sample Standard Deviation** for each array of values. However, it was crashing with a Math Domain Error (taking the square root of a negative number) due to floating-point catastrophic cancellation in its naive one-pass formula: `sqrt((sum(x^2) - (sum(x)^2)/n) / (n-1))`. 
3. The old service also suffered from race conditions and deadlocks when trying to process records concurrently, and struggled with some JSON payloads that contained improperly serialized escape characters.

**Your Task:**
Write a completely new, robust script in the language of your choice (save the source file in `/home/user/solution/` and the executable/run script as `/home/user/solution/run.sh`). 
Your script must:
1. Parse the custom binary format in `/home/user/data/inputs.dat` properly, handling the UTF-16LE encoding.
2. Calculate the Sample Standard Deviation for each record's `values` array. You MUST use a numerically stable algorithm (like Welford's online algorithm or a stable two-pass method) to prevent the math domain errors caused by catastrophic cancellation on datasets with very high means and low variances.
3. If a dataset has fewer than 2 values, its standard deviation should be output as `null`.
4. Process the data efficiently.
5. Write the final output to `/home/user/output.jsonl`. Each line must be a valid UTF-8 JSON object in exactly this format: `{"id": "A1", "std_dev": 1.234567}` (round standard deviation to 6 decimal places). The output must be sorted alphabetically by `id`.

Fix the math, fix the encoding, and save the day. Create `/home/user/output.jsonl` with the correct results.