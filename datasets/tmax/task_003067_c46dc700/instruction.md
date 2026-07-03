You are an MLOps engineer tasked with analyzing the stability of experiment artifacts. A recent model training experiment crashed, and you need to estimate its likely performance based on similar historical experiments using a reproducible pipeline.

You have been provided with a dataset of past experiment artifacts at `/home/user/experiments.jsonl`. Each line is a JSON object with `exp_id`, `description`, and `metrics` (an array of accuracy scores across different cross-validation folds).

Your target failed experiment has the following description:
`"ResNet50 using AdamW optimizer, learning_rate=0.001, batch=32"`

Write a Python script at `/home/user/analyze.py` that does the following:
1. **Embedding Computation and Retrieval**: 
   - Read the historical experiments.
   - Use `scikit-learn`'s `TfidfVectorizer` (initialized with `lowercase=True` and `stop_words='english'`) to compute vector representations for all historical experiment descriptions PLUS the target description.
   - Compute the cosine similarity between the target description and all historical descriptions.
   - Identify the top 3 most similar historical experiments (by `exp_id`).

2. **Data Aggregation**:
   - Extract the `metrics` lists from these top 3 experiments and concatenate them into a single combined 1D numpy array.

3. **Reproducible Bootstrap Analysis**:
   - To ensure strict reproducibility, you must configure your numerical pipeline. Set `numpy.random.seed(42)` exactly once, immediately before running the bootstrap loop.
   - Perform a bootstrap analysis with exactly `10000` iterations to estimate the mean performance.
   - In each iteration, sample with replacement from the combined metrics array. The size of the sample should equal the size of the combined metrics array.
   - Calculate the mean of each sample.
   - Calculate the overall mean of the bootstrap means, as well as the 95% confidence interval (the 2.5th and 97.5th percentiles of the 10,000 bootstrap means) using `numpy.percentile`.

4. **Reporting**:
   - Output the results to a JSON file at `/home/user/report.json`.
   - The JSON file must have exactly the following keys and format:
     ```json
     {
       "top_3_exp_ids": ["EXP_X", "EXP_Y", "EXP_Z"],
       "bootstrap_mean": 0.1234,
       "ci_lower": 0.1200,
       "ci_upper": 0.1250
     }
     ```
   - Float values should be rounded to 4 decimal places. The `top_3_exp_ids` list should be ordered by cosine similarity descending.

You can run your script using `python3 /home/user/analyze.py`.