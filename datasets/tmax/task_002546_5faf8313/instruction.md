You are an AI assistant helping a data researcher organize a collection of textual datasets. The researcher wants to classify short text snippets using a lightweight, reproducible pipeline written entirely in Rust, avoiding heavy external dependencies.

Your task is to build a Rust application that performs feature engineering, embedding computation, and cross-validation to tune a hyperparameter for a K-Nearest Neighbors (K-NN) classifier.

**Requirements:**

1. **Project Setup:**
   Create a new Rust binary project at `/home/user/dataset_organizer`.

2. **Data Ingestion:**
   The researcher has placed a dataset at `/home/user/data.csv`. It has two columns: `text` and `label`. 
   Read this CSV file. You may use standard library features (no external CSV crates are strictly required if you parse it manually, but you can use `csv` if you configure `Cargo.toml`).

3. **Feature Engineering (Embedding Computation):**
   Map each `text` into a 5-dimensional numerical vector. The 5 dimensions represent the frequency (count) of the following specific character bigrams (case-insensitive):
   - Index 0: "th"
   - Index 1: "he"
   - Index 2: "in"
   - Index 3: "er"
   - Index 4: "an"
   *(For example, the text "The hero" has "th" (1), "he" (2), "er" (1) -> vector `[1, 2, 0, 1, 0]`)*

4. **K-NN and Cross-Validation (Hyperparameter Tuning):**
   Implement a Leave-One-Out Cross-Validation (LOOCV) pipeline to evaluate a K-Nearest Neighbors classifier based on the Euclidean distance between these 5-D vectors. 
   - Test hyperparameter `k` for the values: `k = 1`, `k = 2`, and `k = 3`.
   - For a given text, find the `k` closest *other* texts in the dataset.
   - The predicted label is the most frequent label among those `k` neighbors. (In case of a tie, default to the label that appears first alphabetically).
   - Calculate the LOOCV accuracy (number of correct predictions / total texts) for each `k`.

5. **Output Generation:**
   Find the `k` that yields the highest accuracy (if there's a tie, pick the smallest `k`).
   Write a JSON file to `/home/user/best_model.json` with the following exact format:
   ```json
   {
     "best_k": 2,
     "accuracy": 0.85
   }
   ```
   (Replace `2` and `0.85` with the actual best `k` and its corresponding accuracy as a float).

6. **Reproducibility:**
   Create a bash script at `/home/user/run_pipeline.sh` that builds the Rust project in release mode and executes it to produce the `best_model.json` file. Ensure the script is executable.

You have all the tools necessary. Good luck!