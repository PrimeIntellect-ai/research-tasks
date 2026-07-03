You are a Machine Learning Engineer tasked with preparing training data and building a baseline model. You have two data sources that need to be merged and processed.

Data sources:
1. `/home/user/data/documents.json`: A JSON file containing an array of objects with `id` (int), `text` (string), and `label` (int).
2. `/home/user/data/metadata.csv`: A CSV file containing `id` (int) and `category_id` (int).

There is a known issue: the `metadata.csv` file has some missing values in the `category_id` column.

Your objective is to complete the following pipeline:
1. **Join Data**: Merge the metadata into the documents data using the `id` column.
2. **Handle Missing Values**: Fill any missing `category_id` values with `-1`.
3. **Data Type Consistency**: Ensure that `category_id` is strictly an integer. (Beware: data processing libraries often silently cast columns with missing values to floats, which breaks our downstream strict-typed embedding lookup service).
4. **Dimensionality Reduction**: Compute TF-IDF features on the `text` column (use English stop words, max_features=50), then apply Truncated SVD to reduce it to exactly 3 components (`svd_0`, `svd_1`, `svd_2`). Set the random state to `42` for SVD.
5. **Model Training**: Train a standard Logistic Regression model (default parameters, `random_state=42`) using the 3 SVD features and the `category_id` feature to predict the `label`. Use the entire dataset for training.
6. **Output Export**: 
   - Export the processed features to `/home/user/output/features.jsonl` (JSON Lines format). Each line must be a JSON object containing `id`, `svd_0`, `svd_1`, `svd_2`, and `category_id`. The `category_id` value MUST be serialized as an integer (e.g., `10`, not `10.0`).
   - Export the model's training accuracy (as a float between 0 and 1) to `/home/user/output/accuracy.txt`.

Ensure your output directories exist before writing to them. You may use any combination of Python and shell commands to accomplish this.