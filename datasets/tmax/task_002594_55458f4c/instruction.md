You are an AI assistant helping a mathematics researcher analyze a dataset of mathematical paper abstracts and citation counts. The researcher wants to test if papers with similar abstract topics to a seminal paper ("math_001") have a statistically different number of citations compared to the rest of the dataset.

Your task is to build an end-to-end data pipeline that joins the data, computes text embeddings, retrieves the most similar papers, performs a hypothesis test, and tracks the experiment results. 

The raw data is located in `/home/user/math_dataset/`:
- `/home/user/math_dataset/abstracts/`: Contains 200 text files named `math_001.txt` through `math_200.txt`.
- `/home/user/math_dataset/metadata.csv`: Contains two columns: `file_id` (e.g., "math_001") and `citations` (integer).

Please complete the following steps using the language of your choice (Python is recommended):

1. **ETL & Multi-source Joining:** Read all 200 text files and join them with the citation metadata using `file_id`. 
2. **Embedding Computation:** 
   - Compute TF-IDF features for the text abstracts. You MUST use the following exact parameters: `lowercase=True`, `stop_words='english'`, and `max_features=500`.
   - Reduce the dimensionality of the TF-IDF vectors using Truncated SVD (LSA) to create dense embeddings. You MUST use `n_components=10` and `random_state=42` to ensure deterministic results.
3. **Retrieval:** Calculate the cosine similarity between the embedding of the query paper (`math_001`) and all other papers. Identify the top 20 most similar papers to `math_001` (excluding `math_001` itself).
4. **Hypothesis Testing:** Conduct a Welch's two-sample t-test (unequal variances) to compare the mean citations of the top 20 retrieved papers versus the remaining 179 papers. Also, calculate the 95% confidence interval for the difference in means (`Mean_Top20 - Mean_Rest`).
5. **Experiment Tracking:** Output your final results to a JSON file at `/home/user/experiment_log.json` with the following precise schema (all float values rounded to 4 decimal places):
```json
{
  "top_20_mean_citations": 0.0000,
  "rest_mean_citations": 0.0000,
  "t_statistic": 0.0000,
  "p_value": 0.0000,
  "ci_lower": 0.0000,
  "ci_upper": 0.0000
}
```

Ensure your code is reproducible and runs directly in the terminal without requiring GUI interaction.