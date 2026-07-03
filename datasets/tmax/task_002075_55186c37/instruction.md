You are an AI assistant helping a data science researcher organize and analyze a messy dataset of experimental results. The researcher wants to build a reproducible data processing pipeline in Rust that strictly enforces data schemas and performs bootstrap sampling.

Your task is to write a Rust program that cleans the data, calculates bootstrap confidence intervals, and outputs the results as a JSON file.

### Prerequisites & Setup
1. A raw dataset is located at `/home/user/experiments.csv`.
2. You must create a new Rust project at `/home/user/pipeline` using Cargo.
3. You may use standard crates like `csv`, `serde`, and `serde_json`.

### Pipeline Specifications

**1. Data Schema Enforcement**
The input CSV contains the following columns:
* `experiment_id` (String)
* `temperature` (Float)
* `particle_count` (Integer, but contains missing values like `"NA"`, `"N/A"`, or empty strings)

A naive tool might silently cast `particle_count` to floats to handle `NaN`s, but you must strictly enforce the schema in Rust (e.g., using `Option<i32>` or `Option<u32>` for the count). 
* Drop any rows where `particle_count` is missing or invalid.

**2. Tabular Transformation**
* Group the valid rows by `experiment_id`.
* For each group, extract the `temperature` values. Keep them in the order they appeared in the original CSV.

**3. Deterministic Bootstrap Sampling**
To ensure strict reproducibility without relying on version-specific `rand` crates, implement your own Linear Congruential Generator (LCG) with the following parameters:
* $m = 2^{31}$ (modulus)
* $a = 1103515245$ (multiplier)
* $c = 12345$ (increment)
* Initial seed $X_0 = 42$

*Note: Use a single, global LCG state that persists across all samples and all experiments. Process experiments in alphabetical order of their `experiment_id`.*

For each `experiment_id`:
* Let the valid temperatures for this experiment be an array `T` of length `L`.
* Generate 1000 bootstrap samples. Each sample consists of drawing `L` items from `T` with replacement.
* To draw a single item, advance the LCG state to $X_{n+1} = (a \cdot X_n + c) \pmod m$. The index of the drawn item is $X_{n+1} \pmod L$. 
* Calculate the mean of the `L` items for each of the 1000 bootstrap samples.

**4. Aggregation and Output**
* For each `experiment_id`, sort the 1000 bootstrap means in ascending order.
* Extract the 2.5th percentile (index 25) and the 97.5th percentile (index 975).
* Calculate the overall simple mean of the original `T` array.
* Output the results to `/home/user/summary.json` in the following format (round all floats to 2 decimal places in the JSON):

```json
{
  "exp_A": {
    "mean": 12.34,
    "ci_lower": 11.20,
    "ci_upper": 13.50,
    "valid_samples": 5
  },
  "exp_B": {
    ...
  }
}
```

Write the Rust code, build it, and run it so that `/home/user/summary.json` is generated successfully.