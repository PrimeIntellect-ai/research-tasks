You are tasked with building a robust data processing and statistical modeling pipeline in Rust. 

You have a dataset of text documents in `/home/user/data.txt` (one document per line). As a data scientist, you need to clean this dataset, extract features, and perform probabilistic analysis.

Write a Rust project in `/home/user/pipeline` (you will need to create the Cargo project) that does the following when run:

1. **Tokenization and Dataset Preparation**:
   - Read `/home/user/data.txt`.
   - Tokenize each line by converting to lowercase, removing all non-alphabetic characters (except whitespace), and splitting by whitespace. Ignore empty tokens.

2. **Feature Engineering and Selection**:
   - Count the frequency of all unique tokens across the entire dataset.
   - Select the top 10 most frequent words. If there are ties, resolve them by sorting alphabetically.

3. **Bayesian Inference**:
   - For each of the top 10 words, treat its presence in a document as a Bernoulli trial (1 if the word appears at least once in the document, 0 otherwise).
   - Assume a Beta(2, 2) prior distribution for the probability of presence $p$ for each word.
   - Calculate the expected value (mean) of the posterior distribution for $p$ for each of the top 10 words given the entire dataset.

4. **Sampling and Bootstrap Methods**:
   - Perform 1000 bootstrap resamples of the document dataset (sample with replacement, where each bootstrap sample has the same number of documents as the original dataset).
   - *Requirement for reproducibility*: Use the `rand` crate (version 0.8) with `rand::rngs::StdRng` and seed it with `42` (`StdRng::seed_from_u64(42)`). When creating a bootstrap sample, generate the document indices by calling `rng.gen_range(0..N)` where `N` is the total number of documents, exactly `N` times per resample. Do this for 1000 resamples in order.
   - For each bootstrap sample, recalculate the posterior mean for the top 10 words using the same Beta(2, 2) prior.
   - Calculate the average of these 1000 bootstrap posterior means for each word.

5. **Output**:
   Write the results to `/home/user/results.json` matching this exact structure:
   ```json
   {
     "top_words": ["word1", "word2", ...],
     "posterior_means": [0.123, 0.456, ...],
     "bootstrap_means": [0.124, 0.455, ...]
   }
   ```
   (Round all floating point values to 4 decimal places in the JSON).

Run your Rust program so that `/home/user/results.json` is generated successfully.