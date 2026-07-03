I am a researcher organizing a large dataset of textual logs. I started writing a Rust pipeline to process the metadata, compute basic embeddings, and assign a regression score to each log. However, I am running into a silent data corruption issue inspired by a classic pandas pitfall: missing integer IDs are causing the parsing logic to silently fail or cast things incorrectly.

I have a basic Rust project in `/home/user/log_pipeline` and an input dataset at `/home/user/data/logs.csv`.

Your task is to fix the pipeline and generate the final processed dataset. 

Requirements:
1. **Fix the Schema:** The input CSV has three columns: `id` (integer), `group_id` (integer, but sometimes empty/missing), and `content` (string). Currently, the missing `group_id`s might be causing silent errors or being parsed as floats. Modify the Rust code to strictly parse `group_id` as an `Option<i32>`.
2. **Embedding Computation:** For each row, compute a 3-dimensional normalized frequency "embedding" based on the `content` string. The dimensions should be the occurrences of the characters `'x'`, `'y'`, and `'z'` (case-insensitive), divided by the total length of the `content` string. 
3. **Regression:** Using the `ndarray` crate (configure it in `Cargo.toml`), compute a regression score for each row. The score is the dot product of the 3D embedding and the weight vector `[0.5, 0.3, -0.2]`. 
4. **Reproducibility Test:** Ensure the output is deterministic. Write the processed records to `/home/user/processed_logs.csv` with the header `id,safe_group_id,score`. 
   - `safe_group_id` should be the integer `group_id`, or `-1` if it was missing.
   - `score` should be formatted to 4 decimal places.

Run your Rust pipeline to generate the final `/home/user/processed_logs.csv`.