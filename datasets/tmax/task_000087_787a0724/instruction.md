You are a data analyst tasked with building a lightweight feature engineering and hyperparameter tuning pipeline in C. 

You have been provided with a dataset of 100 text reviews at `/home/user/dataset.csv`. The file has no header and is formatted as:
`label,text`
Where `label` is either `0` or `1`, and `text` consists of lowercase alphabetic characters and spaces.

Your goal is to write a C program that performs tokenization, feature extraction, and grid search with 5-fold cross-validation to find the optimal hyperparameters for a simple rule-based classifier.

Here are the requirements for your C program (`/home/user/cv_tune.c`):
1. **ETL & Tokenization**: Read `/home/user/dataset.csv`. For each row, split the `text` into tokens using the space character (` `) as the delimiter.
2. **Feature Extraction**: Compute a single integer feature for each row: the count of tokens that have a length strictly greater than `M` characters.
3. **Model**: A simple classifier that predicts `1` if the extracted feature count is greater than or equal to `T`, and predicts `0` otherwise.
4. **Cross-Validation & Tuning**: Perform a grid search over the hyperparameters `M` $\in \{2, 3, 4, 5\}$ and `T` $\in \{1, 2, 3\}$. 
   - Use sequential 5-fold cross-validation (no shuffling). Since there are 100 rows, Fold 0 uses rows 0-19 as the validation set, Fold 1 uses rows 20-39, and so on.
   - For each `(M, T)` pair, compute the accuracy on each of the 5 validation folds, then calculate the mean validation accuracy.
5. **Selection**: Find the `(M, T)` pair that yields the highest mean validation accuracy. If there is a tie, prefer the smallest `M`, then the smallest `T`.

Write your C code to `/home/user/cv_tune.c`, compile it, and run it. 
Your program must output the best hyperparameter pair to a file named `/home/user/result.txt` in the exact format:
`M,T`
(e.g., `4,2` with no spaces or additional text).