You are a data researcher organizing sensor datasets and building a custom performance-optimized evaluation pipeline. 

Your objective is to build an ETL script to clean raw logs, and then write a C program that performs cross-validation and hyperparameter tuning for a Ridge Regression model.

**Phase 1: ETL Pipeline**
You have a raw log file at `/home/user/raw_data.txt`. Each line contains sensor readings in this format:
`[TIMESTAMP] STATUS=<OK|ERROR> X=<float> Y=<float> ID=<int>`

Write a bash script at `/home/user/etl.sh` that:
1. Filters out any lines where `STATUS=ERROR`.
2. Extracts only the `X` and `Y` values for the valid lines.
3. Saves the output to `/home/user/clean_data.csv` in the format `X,Y` (no spaces, comma-separated, no headers). Maintain the original order of the rows.

**Phase 2: Numerical C Code & Cross-Validation**
Write a C program at `/home/user/tune.c` that reads `/home/user/clean_data.csv`. 
The program must perform 5-fold cross-validation to tune the regularization hyperparameter $\lambda$ for a 1-dimensional Ridge Regression model without an intercept.

Model definition: 
$\hat{y} = w \cdot x$

Training formula for a given training set and $\lambda$:
$w = \frac{\sum x_i y_i}{\sum x_i^2 + \lambda}$

Cross-validation details:
1. The dataset will have exactly 50 clean rows. Split the data into 5 consecutive equal-sized folds (Fold 1: rows 1-10, Fold 2: rows 11-20, etc.).
2. Evaluate the following candidate values for $\lambda$: `0.1`, `1.0`, `10.0`, `100.0`.
3. For each $\lambda$, iterate through the 5 folds. In each iteration, use 1 fold as the validation set and the remaining 4 folds as the training set.
4. Calculate $w$ on the training set. Then, compute the Sum of Squared Errors ($SSE = \sum (y_i - \hat{y}_i)^2$) on the validation set.
5. Accumulate the validation SSE across all 5 folds to get the Total CV SSE for that $\lambda$.
6. Find the $\lambda$ that produces the lowest Total CV SSE.

Your C program must:
- Include the standard math library (`math.h`).
- Be compiled into an executable named `/home/user/tune` (use `gcc -O2 -o tune tune.c -lm`).
- Write the best $\lambda$ to `/home/user/best_lambda.txt` formatted to 1 decimal place (e.g., `10.0`).

Run your pipeline to generate the final `best_lambda.txt`.