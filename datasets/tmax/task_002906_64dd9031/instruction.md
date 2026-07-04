You are a data analyst tasked with processing a dataset of messy customer feedback.

You have a CSV file located at `/home/user/feedback.csv`. It contains three columns: `id`, `category`, and `comment`.
The `comment` column contains free-text reviews, and somewhere within the text, users usually leave a rating in the format `X/Y` (e.g., "Rating: 4.5/5", "Score: 3/10", or just "4/5 stars"). 

Your task is to write a Python script that processes this file and performs the following operations:
1. **Extraction**: Extract the rating `X/Y` from the `comment` column. `X` and `Y` can be integers or decimals. If multiple matches exist, use the first one. If no match exists, the record is invalid.
2. **Validation**: Check that the rating is mathematically valid and logical. Specifically, drop records where:
   - No rating was found in the text.
   - `Y` (the denominator) is equal to `0`.
   - The normalized score (`X / Y`) is strictly greater than `1.0` or strictly less than `0.0`.
3. **Normalization**: For valid records, compute the normalized score as the float value of `X / Y`.
4. **Aggregation**: Group the valid records by `category`. Calculate the average (mean) normalized score and count the total number of valid reviews for each category.

Save your final results to a JSON file at `/home/user/summary.json`. The JSON file should be a dictionary mapping each `category` name to its aggregated stats, using the keys `"mean_score"` (rounded to 4 decimal places) and `"valid_count"`.

Example output format for `/home/user/summary.json`:
```json
{
  "Electronics": {
    "mean_score": 0.6000,
    "valid_count": 2
  },
  "Home": {
    "mean_score": 0.4000,
    "valid_count": 2
  }
}
```

Ensure your script is self-contained and leaves `/home/user/summary.json` strictly formatted as requested.