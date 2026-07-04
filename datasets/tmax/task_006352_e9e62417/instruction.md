You are a data engineer building ETL pipelines. One of the steps in your pipeline tokenizes raw log text and extracts token frequencies to detect anomalies. Recently, a silent misconfiguration caused the tokenization step to produce empty outputs (similar to a visualization script producing blank plots without throwing errors). 

To prevent this, you need to write a Rust utility that tests the numerical accuracy and stability of our tokenization and frequency estimation using bootstrap resampling.

Create a Rust project at `/home/user/etl_tester`.

Write a program in this project that does the following:
1. **Dataset Preparation & Tokenization**: 
   - Read the dataset located at `/home/user/data/logs.jsonl`. Each line is a JSON object with a `text` field.
   - Tokenize the `text` field: convert to lowercase, split by whitespace, and remove any non-alphanumeric characters from each token (keep only `a-z` and `0-9`). Filter out any tokens that become empty strings.
   
2. **Sampling and Bootstrap Methods**:
   - Implement bootstrap resampling to estimate the frequency of the target token: `"critical"`.
   - Perform `B = 1000` bootstrap iterations.
   - In each iteration, sample $N$ records with replacement from the original dataset, where $N$ is the total number of records in `logs.jsonl`.
   - For each bootstrap sample, compute the frequency of the token `"critical"`: (Total occurrences of "critical" in the sample) / (Total valid tokens in the sample).
   - Use `rand::rngs::StdRng` seeded with `42` for your random number generation (from the `rand` crate).
   
3. **Numerical Accuracy Testing**:
   - Calculate the mean and the standard deviation (standard error) of these 1000 frequency estimates.
   - Save the final output to `/home/user/etl_tester/output.json` in the following exact format:
     ```json
     {
       "mean_frequency": 0.012345,
       "standard_error": 0.001234
     }
     ```

Make sure your Rust project is properly initialized and can be run with `cargo run`. You may use the `serde_json` and `rand` crates.