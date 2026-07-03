You are an MLOps engineer tasked with building an artifact tracking and analysis pipeline for a set of machine learning experiments.

We have a collection of experiment artifact logs located in `/home/user/mlops/data/`. There are 50 JSON files, each representing a single experiment run. Each file has the following format:
`{"id": "exp_XX", "weights": [w1, w2, w3, w4], "error_rate": 0.XX}`

Your task is to create a Rust-based ETL and analysis pipeline to process these artifacts. 

Specifically, you must:
1. Initialize a new Cargo project named `artifact_tracker` inside `/home/user/mlops/`.
2. Write a Rust program in this project that reads all 50 JSON files.
3. **Dimensionality Reduction**: Project the 4D `weights` vector into a 1D scalar for each experiment using a dot product with the fixed projection vector `P = [0.5, -0.5, 0.5, -0.5]`. Let's call this scalar the `projected_weight`.
4. **ETL Pipeline Construction**: Extract the `id`, calculate the `projected_weight`, and extract the `error_rate`. Save this processed dataset to `/home/user/mlops/etl_output.csv` with the header `id,projected_weight,error_rate`. The rows must be sorted by `error_rate` in ascending order.
5. **Regression**: Perform a simple ordinary least squares (OLS) linear regression across all 50 experiments where the independent variable (X) is the `projected_weight` and the dependent variable (Y) is the `error_rate`.
6. Write the calculated slope and intercept of this regression to `/home/user/mlops/report.txt` in exactly this format (rounded to 4 decimal places):
```
Slope: <value>
Intercept: <value>
```

You may use standard Rust crates (like `serde`, `serde_json`, `csv`) by adding them to your `Cargo.toml`. 

Ensure that your compiled Rust binary runs successfully and generates both `/home/user/mlops/etl_output.csv` and `/home/user/mlops/report.txt`.