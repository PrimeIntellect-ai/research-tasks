You are an MLOps engineer analyzing inference benchmark artifacts. Our previous reporting tool is producing empty summaries due to a silent failure in how it handles malformed records.

Your task is to write a Go script at `/home/user/analyze.go` to process an inference experiment log and extract the correct benchmarking metrics.

The input data is located at `/home/user/metrics.jsonl`. Each line is supposed to be a JSON object representing an inference request.

You need to write a Go program that performs the following steps:
1. **Data Schema Enforcement:** Read `/home/user/metrics.jsonl` line by line. Strict schema enforcement is required. A valid record must successfully unmarshal into a structure with exactly these types:
   - `model_id` (string)
   - `features` (an array of exactly 3 floats: `[x, y, z]`)
   - `latency_ms` (float64)
   If a line cannot be parsed, is missing fields, has the wrong types, or the `features` array does not have exactly 3 elements, it is considered *invalid* and must be silently dropped. Count the number of *valid* records.

2. **Feature Engineering & Selection (Linear Algebra):** For each valid record, calculate the L2 norm (Euclidean length) of its `features` vector: $\sqrt{x^2 + y^2 + z^2}$. Keep the record for benchmarking only if its L2 norm is **greater than or equal to 10.0**. Count the number of *selected* records.

3. **Inference Benchmarking:** For the *selected* records, collect their `latency_ms` values. Calculate the 95th percentile (p95) latency. 
   *To ensure deterministic calculation, use this exact method for p95:* Sort the selected latencies in ascending order. The p95 value is the element at index `int(math.Ceil(0.95 * float64(N))) - 1` (where N is the number of selected records, and the array is 0-indexed).

4. **Reporting:** Write the final computed metrics as a formatted JSON file to `/home/user/summary.json`. The JSON must have exactly this structure:
   ```json
   {
     "valid_records": <int>,
     "selected_records": <int>,
     "p95_latency": <float64>
   }
   ```

Run your script to generate the `/home/user/summary.json` file.