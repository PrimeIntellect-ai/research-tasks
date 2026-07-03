You are an MLOps engineer investigating a lost model. A simple linear regression model was deployed, but its source code and weights were accidentally deleted. Fortunately, you have logs of its predictions during a "One-At-A-Time" perturbation experiment, where only one feature was varied at a time relative to a baseline. 

Your task is to write a Rust program that reconstructs the model's weights, engineers a specific new feature, and performs inference on a test set.

Here is the setup. The data is located in `/home/user/experiments/`:

1. `logs.csv`: Contains the perturbation experiment predictions.
   Columns: `run_id`, `x1`, `x2`, `x3`, `y_pred`
2. `metadata.csv`: Contains the execution status of the runs.
   Columns: `run_id`, `status`
3. `test.csv`: Contains new inputs that require predictions.
   Columns: `test_id`, `x1`, `x2`, `x3`

**Requirements:**
1. Create a new Rust project at `/home/user/tracker` (e.g., using `cargo new`).
2. Your Rust program must read the CSV files and **filter out** any runs from `logs.csv` where the corresponding `status` in `metadata.csv` is not exactly `"SUCCESS"`.
3. Reconstruct the weights ($w_1, w_2, w_3$) and bias ($b$) of the linear model $y = w_1 x_1 + w_2 x_2 + w_3 x_3 + b$. The `SUCCESS` rows in `logs.csv` contain a baseline row (where $x_1=0, x_2=0, x_3=0$) and perturbation rows where only one feature is non-zero.
4. For each row in `test.csv`, compute a new engineered feature: $x\_comp = (x_1 \times x_2) + x_3$.
5. Use the reconstructed weights to predict $y\_pred$ for each row in `test.csv`.
6. Output the final predictions to exactly `/home/user/experiments/predictions.json` as a JSON array of objects, structured like this:
```json
[
  {
    "test_id": "t1",
    "x_comp": 4.0,
    "y_pred": -1.5
  }
]
```

You may use standard community crates like `csv` and `serde` in your `Cargo.toml`. Run your Rust program to generate the required JSON file.