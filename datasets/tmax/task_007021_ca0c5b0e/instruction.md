You are a data engineer building a lightweight ETL pipeline that includes a similarity-based recommendation step and numerical accuracy testing.

We have a raw data file located at `/home/user/raw_data.jsonl`. Each line is a JSON object with two keys: `item_id` (integer) and `content` (string).

Your task is to write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:

1. **Extract**: Read the data from `/home/user/raw_data.jsonl`.
2. **Transform (Similarity Search)**: 
   - Use `sklearn.feature_extraction.text.TfidfVectorizer` (with default parameters: `lowercase=True`, `analyzer='word'`, etc.) to convert the `content` into TF-IDF vectors.
   - Compute the pairwise cosine similarity matrix for all items.
3. **Numerical Accuracy Test**: 
   - Before proceeding, programmatically verify that the similarity of every item to itself (the diagonal of the similarity matrix) is exactly `1.0` within a tolerance of `1e-5`. If any value fails this, raise an `AssertionError("Numerical accuracy check failed")`.
4. **Load (Recommendations)**:
   - For each item, identify the *most similar other item* (excluding itself). If there is a tie in similarity scores, pick the tied item with the smallest `item_id`.
   - Write the results to `/home/user/recommendations.csv`.
   - The CSV must have exactly this header: `item_id,rec_id,score`
   - The `score` column must be the cosine similarity rounded to exactly 4 decimal places (e.g., `0.4560`).
   - The CSV rows should be sorted in ascending order by `item_id`.

You must write and execute this script so that `/home/user/recommendations.csv` is correctly generated.