You are an AI assistant acting as a Machine Learning Engineer preparing a custom, high-performance C pipeline for a probabilistic model. 

We need to implement a Gaussian Naive Bayes classifier from scratch in C, complete with k-fold cross-validation, hyperparameter tuning, and experiment tracking.

Here is your task:

1. **Dataset:** A CSV file is located at `/home/user/data.csv`. It contains 100 rows and 3 columns. The first two columns are continuous numerical features ($x_0, x_1$), and the third column is a binary class label ($y \in \{0, 1\}$). There is no header row.

2. **Model:** Implement a Gaussian Naive Bayes classifier in C.
   - For a given training set, compute the prior probabilities for each class: $P(y=c)$.
   - Compute the empirical mean $\mu_{c,f}$ and variance $\sigma^2_{c,f}$ for each class $c \in \{0,1\}$ and feature $f \in \{0,1\}$. 
   *(Note: Use the population variance formula, i.e., divide by $N$, not $N-1$)*.
   - To avoid zero-variance issues, we use a hyperparameter $\epsilon$ (variance smoothing). Add $\epsilon$ to all computed variances: $\sigma^2_{c,f} \leftarrow \sigma^2_{c,f} + \epsilon$.
   - For prediction, assign the class $c$ that maximizes the log-posterior: 
     $\log P(y=c) - \frac{1}{2} \sum_{f=0}^{1} \left( \log(2\pi\sigma^2_{c,f}) + \frac{(x_f - \mu_{c,f})^2}{\sigma^2_{c,f}} \right)$
   - In case of a tie in log-posterior, predict class 0.

3. **Cross-Validation & Hyperparameter Tuning:**
   - Implement 5-fold cross-validation. Since there are 100 rows, divide the data into 5 sequential, non-overlapping chunks of 20 rows each (Fold 0: rows 0-19, Fold 1: rows 20-39, etc., using 0-based indexing).
   - For each fold $k \in \{0, 1, 2, 3, 4\}$, use fold $k$ as the validation set and the remaining 80 rows as the training set.
   - Evaluate three different variance smoothing hyperparameters: $\epsilon \in \{0.01, 0.5, 2.0\}$.
   - For each $\epsilon$, calculate the average cross-validation accuracy (total correct validation predictions across all 5 folds divided by 100).

4. **Experiment Tracking:**
   - Write a C program (`/home/user/train.c`) that performs the above steps.
   - The program must output the best hyperparameter and its corresponding average accuracy to a JSON file at `/home/user/experiment_log.json`.
   - If there is a tie in accuracy between two $\epsilon$ values, choose the smaller $\epsilon$.
   - The JSON file must have exactly this format:
     `{"best_epsilon": 0.00, "best_accuracy": 0.00}` (format floats to 2 decimal places).

Write, compile, and execute the C program to produce the final `experiment_log.json`.