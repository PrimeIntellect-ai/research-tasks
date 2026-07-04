You are a machine learning engineer preparing feature data for a text classification pipeline. We want to identify the most informative tokens for identifying spam messages using a Bayesian approach, specifically by analyzing the log-likelihood ratios from a Naive Bayes model. 

You have a dataset located at `/home/user/emails.csv` containing columns `id`, `text`, and `spam` (1 for spam, 0 for ham).

Your task is to:
1. **Tokenize the dataset:** Convert the `text` column to lowercase, remove all non-alphanumeric characters (keep only a-z, 0-9, and spaces), and split by spaces into a list of tokens. Empty strings should be discarded.
2. **Implement Multinomial Naive Bayes:** Write a script to calculate $P(Token|Class) = \frac{N_{token, class} + \alpha}{N_{class} + \alpha \times V}$ where:
   - $N_{token, class}$ is the count of the token in the given class.
   - $N_{class}$ is the total number of all token occurrences in the class.
   - $V$ is the total number of unique tokens in the entire training dataset.
   - $\alpha$ is the Laplace smoothing parameter.
3. **Cross-Validation:** Evaluate $\alpha \in [0.1, 0.5, 1.0, 2.0, 5.0]$ using 5-fold cross-validation (`sklearn.model_selection.KFold` with `n_splits=5` and `shuffle=False`). For each fold, train on 4 folds and evaluate accuracy on the remaining 1 fold. Calculate the average validation accuracy across the 5 folds for each $\alpha$. Find the `best_alpha` that yields the highest average accuracy (if there is a tie, pick the smallest $\alpha$).
4. **Feature Selection:** Using the `best_alpha`, fit the model on the **entire dataset**. Calculate the absolute Log-Likelihood Ratio (LLR) for every token in the vocabulary: 
   $LLR = |\log(P(Token | spam=1)) - \log(P(Token | spam=0))|$
   Find the top 5 tokens with the highest LLR. Break ties alphabetically.

Save your final results in `/home/user/features.json` with the following strict format:
```json
{
  "best_alpha": 0.5,
  "top_5_tokens": ["token1", "token2", "token3", "token4", "token5"]
}
```