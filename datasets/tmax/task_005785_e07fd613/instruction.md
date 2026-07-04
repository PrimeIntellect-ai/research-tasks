You are an AI assistant helping a Data Engineer fix and build an ETL and recommendation pipeline. 

We have a dataset of product descriptions located at `/home/user/products.csv`. The dataset has three columns: `id`, `split`, and `description`. The `split` column designates whether the item belongs to the `train` or `test` set.

Your task is to implement a simple similarity recommendation script that finds the closest matches for a specific test item, while strictly adhering to best practices to avoid data leakage.

Here are the requirements:
1. Read the dataset `/home/user/products.csv`.
2. Separate the data into a training set and a test set based on the `split` column.
3. Process the `description` column using TF-IDF. 
   - **Crucial constraint:** To prevent data leakage (a common ETL pitfall), you must `fit` your TF-IDF vectorizer **only** on the training set descriptions. Then, `transform` both the training set and the test set using this fitted vectorizer. 
   - Use standard English stop-words removal and convert text to lowercase (if using scikit-learn, `TfidfVectorizer(stop_words='english', lowercase=True)`).
4. For the test item with `id` equal to `test_1`, compute its cosine similarity against all items in the `train` set.
5. Identify the top 3 most similar `train` items based on the cosine similarity scores.
6. Save the results to a JSON file at `/home/user/recommendations.json`. The JSON should be a list of dictionaries, ordered by similarity score in descending order. Each dictionary must have two keys: `"id"` (the id of the train item) and `"score"` (the cosine similarity score, rounded to exactly 4 decimal places).

Example of expected JSON format:
```json
[
  {"id": "train_X", "score": 0.8521},
  {"id": "train_Y", "score": 0.4310},
  {"id": "train_Z", "score": 0.1105}
]
```

You may use any programming language or libraries (e.g., Python with pandas and scikit-learn) you prefer to complete this task. Run your pipeline to generate the final JSON file.