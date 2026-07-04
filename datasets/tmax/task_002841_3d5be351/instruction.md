You are an MLOps engineer tasked with organizing and analyzing a large number of historical experiment artifacts. 

In the `/home/user/artifacts/` directory, there are multiple JSON files representing different machine learning experiment runs. Each JSON file contains metadata about an experiment, including its `experiment_id`, `hyperparameters`, `metrics`, and `status`.

Your goal is to build a lightweight ETL pipeline and retrieval system in Python to find the most similar successful experiments to a new target configuration.

Please perform the following steps:

1. **Extract and Filter**: Read all JSON files in `/home/user/artifacts/`. Filter out any experiments where the `status` is NOT `"SUCCESS"`.
2. **Transform (Feature Engineering)**: For each successful experiment, convert its `hyperparameters` dictionary into a single normalized string. The string must be constructed by sorting the dictionary keys alphabetically and joining them in the format `key=value`, separated by a single space. For example, `{"optimizer": "adam", "lr": 0.01, "batch_size": 64}` becomes `"batch_size=64 lr=0.01 optimizer=adam"`.
3. **Embed**: Use `scikit-learn`'s `TfidfVectorizer` to compute embeddings for these hyperparameter strings. You must configure the vectorizer exactly as follows: 
   - `analyzer='char_wb'`
   - `ngram_range=(2, 3)`
   - `lowercase=True`
4. **Retrieve**: We want to find the top 3 successful experiments that are most similar to the following target hyperparameter configuration:
   `{"batch_size": 32, "lr": 0.005, "optimizer": "adam", "dropout": 0.2}`
   Normalize this target configuration using the exact same transformation rule as above, and compute its embedding using the fitted vectorizer. Calculate the cosine similarity between the target embedding and all the successful experiment embeddings.
5. **Report**: Create a file named `/home/user/top_experiments.txt`. Write the `experiment_id` of the top 3 most similar successful experiments to this file, ordered from highest similarity to lowest similarity. Each `experiment_id` should be on a new line.

Constraints:
- Only use standard Python libraries, `numpy`, and `scikit-learn`.
- Do not modify the original JSON files.