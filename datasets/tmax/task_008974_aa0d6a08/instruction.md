You are a machine learning engineer preparing a training dataset. You need to write a Rust program that joins two data sources, performs a deterministic bootstrap sampling, validates the generated data, and outputs the final metrics. 

Currently, the data generation pipeline is broken (it produces empty datasets due to a join misconfiguration), so you need to write a standalone Rust script from scratch to replace it.

**Data Sources:**
Assume two CSV files exist in `/home/user/data/` (you should create these for your own testing):

1. `/home/user/data/users.csv`
```csv
id,factor
1,1.5
2,2.0
3,0.8
4,1.2
5,3.0
```

2. `/home/user/data/scores.csv`
```csv
user_id,score
2,20.0
3,50.0
4,15.0
5,10.0
6,100.0
```

**Requirements:**
1. Initialize a new Rust project at `/home/user/data_prep`.
2. Write a Rust program (`src/main.rs`) that performs an inner join of the two datasets on `id == user_id`.
3. For each joined record, compute a combined metric: `combined = factor * score`.
4. Sort the joined records by `id` in ascending order to create a stable, deterministic array of `combined` metrics. Let `N` be the number of joined records.
5. Generate exactly 3 bootstrap samples (each of size `N`). Instead of using a random number generator (which can vary across crates and versions), use the following deterministic pseudo-random formula to select the index of the item from the sorted joined array:
   For each sample `sample_idx` from `0` to `2`:
     For each row `i` from `0` to `N - 1`:
       `index = ( (i + 1) * (sample_idx + 2) * 17 ) % N`
       Add the combined metric at `index` to the current bootstrap sample.
6. For each of the 3 bootstrap samples, calculate the mean of the combined metrics.
7. **Validation:** Only keep means that are strictly greater than `0.0`. 
8. Write the valid means to `/home/user/means.txt`, with one mean per line, formatted to exactly two decimal places (e.g., `12.34`).

Compile and run your Rust program to generate the `/home/user/means.txt` file.