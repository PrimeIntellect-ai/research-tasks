You are assisting a researcher in organizing and preprocessing a dataset of user behavior logs. The researcher needs a Python script to clean the data, map categorical events to integer token IDs, and generate low-dimensional embeddings representing user behavior.

The raw data is located at `/home/user/raw_events.csv` with the following columns:
`user_id` (integer)
`timestamp` (string/datetime)
`event_type` (string, but contains missing values)

Write a Python script at `/home/user/prepare_dataset.py` that performs the following pipeline:

1. **Data Transformation & Tokenization**: 
   - Sort the records chronologically by `timestamp` for each user.
   - Map each unique valid `event_type` to a unique integer ID starting from `1` (e.g., 1, 2, 3...). 
   - Missing `event_type` values (empty strings or NaNs) must be assigned the integer token ID `0`.
   - Aggregate the data so that each `user_id` has a chronological list of integer token IDs. 
   - **Crucial**: The token IDs in your final sequence must be strict Python integers. Do not allow Pandas' silent NaN-upcasting to float (e.g., `1.0`, `2.0`) to pollute the final token sequences.

2. **Feature Engineering & Dimensionality Reduction**:
   - Create a user-token frequency matrix (rows = users, columns = token IDs 0 through N, values = count of times that user triggered that token).
   - Use `sklearn.decomposition.PCA` with `n_components=2` and `random_state=42` on this frequency matrix to generate a 2D embedding for each user.

3. **Output**:
   - Save the results to `/home/user/processed_users.json`.
   - The JSON must be a dictionary mapping the string representation of `user_id` to an object containing `"tokens"` (the chronological list of integer IDs) and `"embedding"` (the 2D PCA embedding as a list of two floats, rounded to 4 decimal places).

Example output format for `/home/user/processed_users.json`:
```json
{
  "1": {
    "tokens": [1, 2, 0, 3],
    "embedding": [0.1234, -0.5678]
  },
  "2": {
    "tokens": [2, 1, 1],
    "embedding": [-0.4321, 0.9876]
  }
}
```

Ensure your script handles dependencies appropriately (you can install standard data science packages like `pandas` and `scikit-learn` if needed). Execute your script to produce the final JSON file.