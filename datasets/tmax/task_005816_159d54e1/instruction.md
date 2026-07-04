You are a data analyst optimizing a similarity search algorithm. You have been given two CSV files containing feature vectors:
1. `/home/user/data/query.csv`: Contains a single vector. The first column is a string ID ("query"), followed by 10 numerical features.
2. `/home/user/data/database.csv`: Contains 1,000 vectors. The first column is an integer ID, followed by 10 numerical features.

Your task is to write a Rust program that performs the following tasks to benchmark inference performance and test numerical accuracy:
1. Parse the CSV files.
2. Compute the cosine similarity between the query vector and every vector in the database.
   Cosine Similarity formula: `(A · B) / (||A|| * ||B||)`
3. Perform this computation *twice* for all 1,000 database vectors:
   - Once parsing the features as `f32` and performing all math in `f32`.
   - Once parsing the features as `f64` and performing all math in `f64`.
4. Measure the execution time of the loop that computes the 1,000 similarities for `f32` and the loop for `f64` (in microseconds).
5. Find the maximum absolute difference between the `f32` similarity and `f64` similarity across all 1,000 comparisons (cast `f32` to `f64` before subtracting to find the absolute difference).
6. Identify the integer ID of the database vector that has the highest cosine similarity to the query vector (based on the `f64` results).

Create a Rust project in `/home/user/sim_search` and ensure your code writes the final output to `/home/user/output/results.json` in the exact following format:

```json
{
  "time_us_f32": <integer_microseconds>,
  "time_us_f64": <integer_microseconds>,
  "max_abs_diff": <float_rounded_to_6_decimal_places>,
  "top_match_id": <integer>
}
```

Make sure the output directory exists before writing to it. You can use standard Rust libraries; external crates like `csv` and `serde_json` are highly recommended. You can run your Rust application using `cargo run --release`.