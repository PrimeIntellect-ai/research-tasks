You are assisting a researcher in organizing and analyzing a text dataset. A preprocessing pipeline previously corrupted the dataset by introducing NaNs into the ID column, which silently converted all integer IDs into floats. 

You need to clean the data, extract features, and validate the dataset against a set of preliminary model predictions.

Here are your instructions:
1. **Data Cleaning**: Read `/home/user/raw_data.csv`. Remove any rows where the `id` column is missing (NaN/null). Convert the `id` column back to integers.
2. **Feature Extraction (Tokenization & PCA)**: 
   - Isolate the `text` column for the cleaned rows.
   - Compute TF-IDF features using standard settings (e.g., scikit-learn's `TfidfVectorizer` with default parameters, which lowercases and tokenizes by word).
   - Perform dimensionality reduction using PCA to reduce the TF-IDF matrix to exactly 2 components (PC1 and PC2). Set `random_state=42` if your PCA implementation requires a seed.
3. **Correlation Analysis**: Compute the Pearson correlation coefficient between the dataset's `value` column (from the cleaned rows) and PC1, as well as between the `value` column and PC2. Take the absolute value of both correlations (to account for PCA sign ambiguity).
4. **Model Output Validation**: Read `/home/user/predictions.json`. This file contains key-value pairs where the key is a stringified integer ID. Count how many of your *cleaned* IDs are completely missing from the keys of `predictions.json`.
5. **Reporting**: Create a JSON file at `/home/user/analysis_summary.json` with exactly the following structure (replace the nulls with your computed numbers, rounding floats to 4 decimal places):
```json
{
  "clean_row_count": null,
  "abs_correlation_pc1": null,
  "abs_correlation_pc2": null,
  "missing_predictions": null
}
```