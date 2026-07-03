You are an AI assistant helping a machine learning engineer prepare training data from a network of sensors. 

We have time-series signal data from several nodes in a sensor network, and we need to extract features for a downstream machine learning model. You will write a Rust program to perform this feature extraction.

I have created a skeleton Cargo project at `/home/user/feature_extractor`.
The input data is located at:
1. `/home/user/data/signals.csv`: A CSV file with columns `node_id`, `time`, and `signal`. (Each node has exactly 128 time steps).
2. `/home/user/data/network.json`: A JSON file representing the network graph as an adjacency list (e.g., `{"0": [1, 2], "1": [0], "2": [0]}`).

Write the Rust code in `/home/user/feature_extractor/src/main.rs` to process this data and output a CSV file at `/home/user/features.csv` with the following columns (in order):
`node_id,degree,dominant_freq_index,ci_lower,ci_upper`

For each node (sorted by `node_id` ascending in the output), compute the following features:
1. **`degree`**: The number of neighbors the node has in `network.json`.
2. **`dominant_freq_index`**: The index of the maximum amplitude in the magnitude spectrum of the node's signal. Use the `rustfft` crate to compute the forward FFT. Ignore the DC component (index 0), and only search indices up to `N/2` (inclusive).
3. **`ci_lower` and `ci_upper`**: The 95% bootstrap confidence interval for the mean of the node's signal. 
   - Perform exactly 1000 bootstrap resamples. For each resample, draw $N$ samples with replacement from the node's signal array and compute the mean.
   - Sort the 1000 means in ascending order.
   - `ci_lower` is the 25th element (index 24, assuming 0-indexed), and `ci_upper` is the 975th element (index 974).
   - *Deterministic requirement*: To ensure reproducibility, use `rand::rngs::StdRng` initialized with `SeedableRng::seed_from_u64(node_id as u64)`. When drawing random indices for the resample, use `rng.gen_range(0..N)`.

You may edit `/home/user/feature_extractor/Cargo.toml` to add necessary dependencies (e.g., `csv`, `serde`, `serde_json`, `rustfft`, `num-complex`, `rand`). After writing the code, build and run it so that `/home/user/features.csv` is generated.