You are a Machine Learning Engineer preparing a C++ pipeline for a classification task. You have been provided with a raw dataset at `/home/user/dataset.csv`. 

Due to a upstream data integrity issue, some integer features have been corrupted with `"NaN"` strings.

Your task is to write a C++ program from scratch (`/home/user/pipeline.cpp`) that performs the following steps:

1. **Data Cleaning**: Parse `/home/user/dataset.csv`. The CSV has three columns: `Feature_A`, `Feature_B`, and `Label`. The first line is the header. Drop any rows where `Feature_A` or `Feature_B` contains the exact string `"NaN"`. Store the remaining rows as integers.
2. **Correlation Analysis**: Calculate the Pearson correlation coefficient ($r$) between `Feature_A` and `Feature_B` on the cleaned dataset.
3. **Classification & Cross-Validation**: Implement a K-Nearest Neighbors (KNN) classifier using standard Euclidean distance. To resolve ties in distance, prefer the point that appears first in the dataset. To resolve ties in class voting, prefer class `1` over class `0`.
4. **Hyperparameter Tuning**: Perform 5-fold cross-validation on the cleaned dataset to find the optimal $K$ among the candidates `{1, 3, 5, 7}`. 
    * Folds must be contiguous, unshuffled blocks. If the cleaned dataset has $N$ rows, the first fold (test set) is indices `0` to `floor(N/5) - 1`. The second fold is `floor(N/5)` to `2*floor(N/5) - 1`, and so on. The 5th fold takes all remaining elements.
    * For each $K$, calculate the mean accuracy across the 5 folds.

Compile your program using `g++ -O3 pipeline.cpp -o pipeline` and run it.

Your program must output a file strictly named `/home/user/results.txt` with exactly three lines:
Line 1: The Pearson correlation coefficient, rounded to exactly 3 decimal places (e.g., `0.942`).
Line 2: The optimal $K$ value (an integer). If there is a tie in cross-validation accuracy, choose the smaller $K$.
Line 3: The cross-validation accuracy of the optimal $K$, rounded to exactly 3 decimal places (e.g., `0.815`).

No external machine learning libraries (like mlpack) are allowed; you must rely only on the C++ Standard Library.