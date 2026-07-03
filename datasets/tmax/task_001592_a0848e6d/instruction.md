You are helping a data scientist clean a dataset of user profiles, build an ETL pipeline, and generate recommendations.

There are three tasks you need to complete:

1. **Fix the validation script**:
The data scientist wrote a script at `/home/user/scripts/validate.py` to plot the age distribution of the users. However, it currently produces a completely blank plot at `/home/user/data/plot.png`. Modify `/home/user/scripts/validate.py` so that it successfully saves the histogram with the data visible in the PNG file.

2. **Build the ETL pipeline**:
Create a Python script at `/home/user/scripts/etl.py`. This script must:
- Read `/home/user/data/users.csv`.
- Create a combined feature vector for each user. 
- The feature vector must consist of the TF-IDF representation of the `bio` column (using `sklearn.feature_extraction.text.TfidfVectorizer` with all default parameters) followed by an `age_scaled` value (computed exactly as `age / 100.0`).
- Save the results to `/home/user/data/features.parquet`. The Parquet file must contain exactly two columns: `id` (integer) and `feature_vector` (a list or array of floats).

3. **Generate Recommendations**:
Create a Python script at `/home/user/scripts/recommend.py`. This script must:
- Read `/home/user/data/features.parquet`.
- Compute the cosine similarity between the `feature_vector` of the user with `id=101` and all other users in the dataset.
- Find the top 2 most similar users to `id=101` (excluding `101` itself).
- Save the result in JSON format to `/home/user/recommendations.json` with the following exact structure:
  `{"target": 101, "similar": [first_most_similar_id, second_most_similar_id]}`

Run all your scripts to ensure the plot is generated, the parquet file is created, and the JSON file is populated.