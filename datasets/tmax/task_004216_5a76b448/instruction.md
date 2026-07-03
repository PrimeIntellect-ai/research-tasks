You are a Machine Learning Engineer preparing training data and tracking experiment metrics. 

I have a raw dataset file located at `/home/user/dataset.txt`. I need you to write and execute a Rust program at `/home/user/prepare_data.rs` that performs tokenization, calculates a Bayesian posterior probability, and logs the experiment results.

Here are the exact requirements for the Rust program:
1. Read the text from `/home/user/dataset.txt`.
2. Tokenize the text using the following exact steps:
   - Convert the entire string to lowercase.
   - Replace any character that is not an alphanumeric character (a-z, 0-9) with a space (' ').
   - Split the resulting string by whitespace to get a list of tokens.
3. Count the total number of tokens ($N$) and the number of times the exact token `"anomaly"` appears ($k$).
4. Calculate the expected value of the posterior probability of encountering the token `"anomaly"`. Assume a Beta-Binomial model with a Beta(2, 2) prior. 
   - *Hint*: For a Beta($\alpha$, $\beta$) prior, the posterior after observing $k$ successes in $N$ trials is Beta($\alpha + k$, $\beta + N - k$). The expected value of a Beta distribution is its first parameter divided by the sum of both parameters.
5. Output the results as a JSON file to `/home/user/tracking.json` with the following format:
   ```json
   {
     "total_tokens": <integer>,
     "anomaly_count": <integer>,
     "posterior_expected_value": <float>
   }
   ```

You must compile and run the Rust program so that `/home/user/tracking.json` is generated. You can use standard Rust libraries (or `serde_json` if you choose to set up a Cargo project, but a simple standard library file write is fine if you format the JSON manually). If you create a Cargo project, do so in `/home/user/data_prep`.