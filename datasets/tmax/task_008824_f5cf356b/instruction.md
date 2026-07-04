You are a data engineer building an analytics step for an ETL pipeline. We receive raw textual log files and need to monitor the "homogeneity" of these logs over time. You will write a Python script that tokenizes the logs, uses linear algebra to compute their pairwise similarities, and applies bootstrap sampling to estimate the confidence interval of the average similarity.

Here are the specific requirements:

1. **Input Data**: You will find 50 raw text files in the directory `/home/user/raw_data`. 
2. **Tokenization & Vectorization**:
   - Read all files in alphabetical order by filename.
   - For each file, convert the text to lowercase.
   - Remove the following punctuation characters: `.`, `,`, `!`, `?`.
   - Split the text by whitespace to form tokens.
   - Construct a Term Frequency (TF) matrix where rows are documents (in alphabetical order) and columns are the unique vocabulary terms (sorted alphabetically). The values should be the raw count of a term in a document.
3. **Linear Algebra**:
   - Using Numpy, compute the pairwise cosine similarity matrix between all documents. The cosine similarity between two document vectors $u$ and $v$ is $\frac{u \cdot v}{\|u\|_2 \|v\|_2}$. If a document vector has a magnitude of 0, its similarity with any other document should be 0.
4. **Bootstrap Sampling**:
   - Extract the upper triangular elements of the similarity matrix (excluding the diagonal). These represent all unique pairs of documents.
   - Perform bootstrap sampling to estimate the mean similarity. Specifically, draw 1,000 bootstrap samples (with replacement) from these pairwise similarities. The size of each sample should equal the total number of unique pairs.
   - Calculate the mean of each bootstrap sample.
   - Compute the 2.5th and 97.5th percentiles of these 1,000 bootstrap means to form a 95% confidence interval.
   - **Crucial**: Use `numpy.random.seed(42)` immediately before drawing the 1,000 samples to ensure reproducibility. Use `numpy.random.choice` for sampling and `numpy.percentile` with default settings for the percentiles.

5. **Output**:
   - Calculate the overall mean similarity of the unique pairs.
   - Write a JSON file to `/home/user/etl_output.json` with the following structure, rounding all float values to exactly 4 decimal places:
     ```json
     {
       "mean_similarity": 0.1234,
       "ci_lower": 0.1111,
       "ci_upper": 0.1333
     }
     ```

Write and execute the Python script to generate `/home/user/etl_output.json`.