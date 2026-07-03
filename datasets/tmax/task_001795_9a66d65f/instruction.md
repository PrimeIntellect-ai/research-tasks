You are an AI assistant helping a researcher organize and analyze a dataset of research abstracts. 

The researcher has provided a dataset at `/home/user/abstracts.csv` containing the following columns: `id`, `category`, `text`, and `citations`.

Your task is to analyze this dataset by writing a script in a language of your choice to perform the following steps:

1. **Tokenization and Dataset Preparation**:
   - Process the `text` column: Convert everything to lowercase, remove all characters that are not alphanumeric or spaces, and split the text into tokens by spaces.
   - Count the frequencies of all tokens across the entire dataset. Select the top 50 most frequent tokens as your vocabulary (resolve ties arbitrarily or by alphabetical order, but ensure exactly 50 tokens).

2. **Feature Engineering & Linear Algebra**:
   - Create a Document-Term Matrix (Bag-of-Words) where rows are abstracts and columns represent the counts of the top 50 vocabulary tokens.
   - Center the data by subtracting the mean of each column.
   - Apply Principal Component Analysis (PCA) or Singular Value Decomposition (SVD) on the centered data to extract the 1st Principal Component (PC1) for each abstract.

3. **Hypothesis Testing**:
   - Perform a Welch's two-sample t-test (unequal variances) comparing the PC1 values of abstracts in the "Physics" category versus the "Biology" category. Extract the p-value.

4. **Sampling and Bootstrap Methods**:
   - Filter the dataset to include only the "Biology" category.
   - Use bootstrap resampling (10,000 iterations, sampling with replacement) to estimate the 95% confidence interval for the mean of the `citations` column for the "Biology" category. 
   - Use the percentile method (2.5th and 97.5th percentiles).
   - *Crucial*: Set your random seed to `42` right before starting the bootstrap loop so the results are reproducible.

5. **Reporting**:
   - Output your final results to `/home/user/results.json` strictly matching the following format:
   ```json
   {
       "vocabulary_size": 50,
       "pc1_mean_physics": <float>,
       "pc1_mean_biology": <float>,
       "ttest_p_value": <float>,
       "bootstrap_ci_lower": <float>,
       "bootstrap_ci_upper": <float>
   }
   ```
   (Round all floats to 4 decimal places).