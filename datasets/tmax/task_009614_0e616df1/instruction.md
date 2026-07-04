You are a Machine Learning Engineer preparing a dataset for an item-to-item recommendation model. You have been provided with a raw log of user actions on an e-commerce platform. Your goal is to build a Bash-based data processing pipeline that calculates the conditional probability of a user purchasing item Y given that they purchased item X (a simple Bayesian co-occurrence model).

Write a single Bash script at `/home/user/build_model.sh` that does the following:

1. **Tabular Data Transformation:** 
   Read `/home/user/raw_logs.csv`. The file has the header `user_id,item_id,action_type,timestamp`.
   Filter the data to only include rows where `action_type` is exactly `purchase`. Ignore any other actions (e.g., `view`, `click`). Ensure you handle potential duplicate purchases (if a user buys the same item twice, it should only count as one distinct user-item purchase).

2. **Probabilistic Modeling (Bayesian Inference):**
   Calculate the empirical conditional probability $P(Y|X)$ for all pairs of items.
   $P(Y|X) = \frac{\text{Number of unique users who purchased both X and Y}}{\text{Number of unique users who purchased X}}$
   *Note: Do not calculate $P(X|X)$.*

3. **Similarity Search & Model Output Validation:**
   For each item X that was purchased by at least one user, find all other items Y that co-occurred with X. 
   Format the output as a valid JSON file saved to `/home/user/item_probs.json`.
   The JSON must be an object where each key is an `item_id` (X). Its value should be an array of objects representing the recommended items (Y) and their probabilities, sorted by probability in **descending** order. If probabilities are tied, sort by the recommended `item_id` in **ascending** alphabetical order.
   Probabilities must be rounded to exactly 2 decimal places (e.g., `0.75`, `1.00`).

Example expected JSON format for `/home/user/item_probs.json`:
```json
{
  "item_A": [
    {"item": "item_B", "prob": 0.75},
    {"item": "item_C", "prob": 0.33}
  ],
  "item_B": [
    {"item": "item_A", "prob": 1.00}
  ]
}
```

Constraints:
- You must write the logic using Bash and standard POSIX utilities (like `awk`, `sed`, `grep`, `sort`, `uniq`, `jq`). Do NOT use Python, Perl, or other scripting languages.
- Execute your script so that `/home/user/item_probs.json` is generated before you complete the task.