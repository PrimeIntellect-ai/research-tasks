You are an AI assistant helping a researcher organize and analyze a text dataset. The researcher is trying to rank scientific abstracts based on their relevance to the "Machine Learning" category using a Bayesian approach.

The researcher has scattered data across three files:
1. `/home/user/data/abstracts.csv`: Contains the text data. Columns: `id` (integer), `text` (string).
2. `/home/user/data/metadata.jsonl`: Contains the prior probabilities for each document belonging to the ML category. Format: JSON Lines with keys `id` (integer) and `prior` (float representing $P(ML)$).
3. `/home/user/data/likelihoods.json`: Contains the word likelihoods. Format: JSON dictionary where the keys are words, and the values are dictionaries with keys `1` (representing $P(word | ML)$) and `0` (representing $P(word | \text{Not } ML)$).

**Your Task:**
1. Read and join the datasets on the document `id`.
2. Tokenize the `text` of each abstract:
   - Convert all text to lowercase.
   - Remove all non-alphanumeric characters (keep only letters and numbers, replace punctuation with spaces).
   - Split by whitespace to create a list of tokens.
3. For each document, calculate the **Log-Odds** of the document belonging to the ML category, using the Naive Bayes assumption:
   $$\text{LogOdds}(ML | \text{tokens}) = \log\left(\frac{\text{prior}}{1 - \text{prior}}\right) + \sum_{w \in \text{tokens}} \log\left(\frac{P(w | ML)}{P(w | \text{Not } ML)}\right)$$
   *Note: Use the natural logarithm (`math.log` in Python). If a token is NOT found in `likelihoods.json`, ignore it (do not add anything to the sum for that word).*
4. Identify the `id`s of the **top 2** documents with the highest calculated Log-Odds.
5. Save these top 2 `id`s to a text file located at `/home/user/results/top_abstracts.txt`. The file should contain one integer `id` per line, sorted in descending order of their Log-Odds (highest first).

**Environment Setup:**
You must assume the input files already exist in the specified locations. You will need to create the `/home/user/results/` directory if it does not exist before saving the output. Use Python to perform the data joining, tokenization, and mathematical modeling.