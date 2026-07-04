You are an AI assistant helping a data researcher organize and analyze a new repository of dataset descriptions. 

The researcher wants to find datasets that are relevant to a specific query and determine if a manually selected subset of datasets is statistically more relevant to the query than the rest.

Here is the setup:
- `/home/user/word_embeddings.json`: Contains a dictionary mapping words to 10-dimensional embedding vectors.
- `/home/user/query.txt`: Contains the target query text.
- `/home/user/datasets/`: A directory containing 20 text files (`dataset_1.txt` to `dataset_20.txt`), each containing a brief description of a dataset.
- `/home/user/subset.txt`: Contains a list of filenames (one per line) representing a subset of datasets the researcher manually flagged.

Your task is to:
1. **Compute Document Embeddings**: Read the query and all dataset descriptions. Tokenize the text by converting to lowercase, removing all punctuation (using Python's `string.punctuation`), and splitting by whitespace. The embedding of a document/query is the mean of the embeddings of its words. If a word is not in `word_embeddings.json`, ignore it.
2. **Similarity Search**: Calculate the cosine similarity between the query embedding and each dataset embedding.
3. **Hypothesis Testing & Confidence Intervals**: Split the datasets into two groups: those listed in `subset.txt` (Group A) and the rest (Group B). Perform a two-sided Welch's t-test (unequal variances) to compare the similarity scores of Group A vs. Group B. Calculate the 95% confidence interval for the difference in means ($\text{Mean}_A - \text{Mean}_B$).

Output your final results in a JSON file at `/home/user/results.json` with the following precise format:
```json
{
  "top_3_datasets": ["dataset_X.txt", "dataset_Y.txt", "dataset_Z.txt"],
  "mean_diff": 0.12345,
  "p_value": 0.01234,
  "ci_lower": 0.00123,
  "ci_upper": 0.24567
}
```
*Note*: `top_3_datasets` should be ordered from highest to lowest similarity. Round the numerical values to 5 decimal places. Use standard degrees of freedom (Satterthwaite approximation) for the Welch's t-test confidence interval.