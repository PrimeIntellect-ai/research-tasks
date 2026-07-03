You are a data analyst troubleshooting a content recommendation pipeline for a media company. The previous data scientist left behind a script at `/home/user/recommend.py` that processes an article dataset (`/home/user/data/articles.csv`) to compute dataset statistics and make recommendations. 

However, there are two major issues:
1. **Schema Violations:** The script crashes because the newly ingested CSV contains malformed data (missing text, invalid IDs).
2. **Data Leakage:** The script applies `TfidfVectorizer.fit_transform` to the entire dataset *before* splitting it into train and test sets, inflating the evaluation metrics.

Your task is to fix `/home/user/recommend.py` to address these issues and output the correct results.

**Requirements:**

1. **Schema Enforcement:** 
   - Load the CSV file using pandas.
   - Force the `id` column to be numeric. If an `id` cannot be converted to a number, treat it as missing (NaN).
   - Drop any rows that have missing values (NaN/Null) in the `id`, `title`, or `text` columns.
   - Cast the `id` column to integer type.

2. **Fix Data Leakage:**
   - Split the cleaned dataframe into training and testing sets using `sklearn.model_selection.train_test_split` with `test_size=0.25` and `random_state=42`.
   - Initialize a new `TfidfVectorizer`.
   - **Crucially:** `fit` the vectorizer ONLY on the training set's `text`. Then `transform` the training set's `text` and `transform` the test set's `text`.

3. **Compute Metrics:**
   - Calculate the mean cosine similarity of all document pairs within the training set.
   - Calculate the mean cosine similarity of all document pairs within the testing set.
   - Save these two values as a JSON file at `/home/user/metrics.json` with the exact keys `"train_avg_sim"` and `"test_avg_sim"`.

4. **Make a Recommendation:**
   - Using the vectorizer fitted on the training set, transform the new query string: `"Deep learning and neural networks"`
   - Compute the cosine similarity between this query vector and all documents in the **training set**.
   - Find the top 2 most similar articles from the training set.
   - Save these top 2 recommendations to `/home/user/recommendations.csv`. The CSV must contain exactly three columns: `id`, `title`, `similarity` (in that order) and be sorted by `similarity` in descending order.

Run your corrected script to generate `/home/user/metrics.json` and `/home/user/recommendations.csv`.