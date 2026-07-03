You are an AI assistant helping a data analyst. The analyst has a Rust project in `/home/user/text_analyzer` that reads a CSV dataset, computes text embeddings, and performs K-Nearest Neighbors (KNN) classification. 

However, the analyst is facing an issue analogous to a misconfigured plotting backend producing "blank plots" — their Rust program runs, but the embeddings are all outputting as identical zero-vectors due to a bug in the text preprocessing and embedding function. Furthermore, the dataset contains malformed rows, and the cross-validation pipeline is incomplete.

Your task is to fix and complete the Rust project to achieve the following:

1. **Schema Enforcement**: Read `/home/user/dataset.csv`. The expected schema is `id` (integer), `text` (string), and `label` (string). You must filter out any rows where:
   - `id` cannot be parsed as an integer.
   - `text` is completely empty.
   - `label` is missing.
   
2. **Fix the Embedding Computation**: In `src/embedding.rs`, there is an `embed` function. Currently, it fails to process the text correctly and returns zeroes. Fix it so it implements this exact deterministic pseudo-embedding logic:
   - The vector dimension is 5.
   - `vec[0]` = length of the text (as f32).
   - `vec[1]` = number of vowels (a, e, i, o, u, case-insensitive) in the text.
   - `vec[2]` = number of consonants in the text.
   - `vec[3]` = number of whitespace characters.
   - `vec[4]` = sum of ASCII values of all characters modulo 100.
   *(Note: Do not normalize the vector).*

3. **Cross-Validation & Hyperparameter Tuning**: Implement a 5-fold cross-validation over the cleaned dataset to find the best `K` for a K-Nearest Neighbors classifier.
   - Use Euclidean distance to compare embeddings.
   - Evaluate `K` values: `1`, `3`, `5`.
   - To create the 5 folds, do NOT shuffle the cleaned data. Keep the original order of the valid rows, and split them sequentially into 5 chunks (if the number of valid rows is not perfectly divisible by 5, the last chunk should contain the remainder, but for this dataset, it will divide evenly).
   - For each fold `i` (0 to 4), use fold `i` as the validation set, and the remaining 4 folds as the training set.
   - Predict the `label` for each item in the validation set by finding the `K` closest embeddings in the training set. (In case of a tie in labels among the K neighbors, pick the label that appears first alphabetically).
   - Compute the average accuracy across the 5 folds for each `K`.

4. **Output**: Write the best `K` and its corresponding average accuracy to `/home/user/tuning_results.json` in the following format:
   ```json
   {
       "best_k": 3,
       "best_accuracy": 0.85
   }
   ```
   *(If there is a tie for the best accuracy, choose the smaller `K`).*

You must use Rust. You may use standard libraries and the `csv` and `serde` crates (which are already in the `Cargo.toml`). Compile the project using `cargo build --release` and run it to produce the JSON file.