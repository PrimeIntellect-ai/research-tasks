You are a data engineer tasked with building an ETL pipeline that processes customer feedback, computes text embeddings, engineers new similarity features, and performs statistical hypothesis testing.

Your task is to process a dataset of customer feedback located at `/home/user/feedback_data.csv` and generate specific outputs. You may use any programming language, but Python with `pandas`, `scikit-learn`, and `scipy` is highly recommended. 

Here are the precise steps you must implement:

1. **Embedding Computation (ETL)**:
   - Load `/home/user/feedback_data.csv`. The dataset has columns `id`, `category`, and `text`.
   - Compute text embeddings for the `text` column using TF-IDF followed by Truncated SVD (LSA).
   - For TF-IDF, use `stop_words='english'` and leave all other parameters as default.
   - For Truncated SVD, set `n_components=5` and `random_state=42`.

2. **Feature Engineering**:
   - Isolate the embeddings for all rows where `category` is exactly `"Product"`.
   - Compute the centroid (mean vector) of these "Product" embeddings.
   - For *every* row in the dataset (regardless of category), calculate the cosine similarity between the row's embedding and the "Product" centroid.
   - Save the dataset with a new column named `sim_to_product` (rounded to 4 decimal places) to `/home/user/processed_feedback.csv`.

3. **Embedding Retrieval**:
   - Filter the processed dataset for rows where `category` is `"Support"`.
   - Find the top 5 rows with the highest `sim_to_product`.
   - Write the `id`s of these top 5 rows, sorted in descending order of similarity, to `/home/user/top_5_support.txt` (one ID per line).

4. **Hypothesis Testing**:
   - We want to test if the mean `sim_to_product` for the "Product" category is significantly different from the "Support" category.
   - Perform a two-sided Welch's t-test (independent t-test assuming unequal variances) comparing the `sim_to_product` values of "Product" vs. "Support".
   - Calculate the 95% confidence interval for the difference in means (`mean_product - mean_support`).
   - Save the results in `/home/user/stat_results.json` with exactly the following keys, with values rounded to 4 decimal places:
     - `"t_statistic"`
     - `"p_value"`
     - `"ci_lower"`
     - `"ci_upper"`

Make sure to install any required numerical libraries (e.g., `pip install pandas scikit-learn scipy`) before running your scripts.