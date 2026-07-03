You are an AI assistant helping a Machine Learning Engineer fix a data preparation pipeline. 

The engineer has written a Rust project at `/home/user/nlp_prep` to process a tabular dataset (`/home/user/dataset.csv`), tokenize the text, compute basic Bayesian unigram probabilities using Laplace (add-one) smoothing, and track the experiment metrics. 

However, the engineer is complaining about a few issues:
1. **Empty/Blank Experiment Tracking:** Similar to a misconfigured plotting backend returning blank images, the `experiment_metrics.json` file is currently writing `0` for vocabulary size and total tokens, and outputting an empty data file.
2. **Tokenization Aggregation Error:** The tokenizer is treating capitalized and lowercase words as distinct tokens, ruining the aggregation.
3. **Probabilistic Modeling Bug:** The Laplace smoothing implementation is mathematically incorrect. It currently computes `P(w) = (count + 1) / total_tokens`. For proper Bayesian Laplace smoothing, it must be `P(w) = (count + 1) / (total_tokens + vocabulary_size)`.

Your task is to fix the Rust code in `/home/user/nlp_prep/src/main.rs` to address these issues. 

Requirements:
- Read `/home/user/dataset.csv` (which has headers `id,text`).
- Tokenize the `text` column by whitespace and convert all tokens to lowercase.
- Calculate the correct Laplace smoothed probability for each unique token.
- Output the top 3 tokens (sorted by probability descending, then alphabetically ascending for ties) to `/home/user/top_tokens.csv` with the header `token,probability`. Format the probability to exactly 6 decimal places.
- Output the experiment tracking data to `/home/user/experiment_metrics.json` in the exact format: `{"vocab_size": X, "total_tokens": Y}` where X and Y are integers representing the unique lowercased vocabulary size and the total number of words processed, respectively.

Once you have fixed the code, compile and run the project using `cargo run --release` from the `/home/user/nlp_prep` directory to generate the output files.