You are an MLOps engineer tasked with building a lightweight, C-based data pipeline and hyperparameter tuning script that tracks experiment artifacts.

Your goal is to write a C program at `/home/user/train.c` that parses a dataset, cleans it, performs tokenization to extract features, tunes a simple linear model using cross-validation, and saves the experiment artifacts.

You have been given a dataset at `/home/user/dataset.csv` with the following header:
`id,f1,text,label`
Where `f1` is a floating-point feature, `text` is a string, and `label` is an integer (0 or 1).

Your C program must perform the following steps exactly in this order:

1. **Dataset Preparation & Missing Value Handling**:
   - Read `/home/user/dataset.csv`.
   - Some rows have the string `"NA"` in the `f1` column. Calculate the mean of all valid (non-NA) `f1` values.
   - Impute the missing `f1` values by replacing `"NA"` with the computed mean.

2. **Tokenization & Outlier Handling**:
   - For the `text` column, tokenize the string by counting the number of space-separated words. This word count becomes a new integer feature, `f2`.
   - Identify outliers: drop any rows from the dataset where `f2 > 20`.

3. **Model Training & Hyperparameter Tuning (Cross-Validation)**:
   - We are using a simple linear threshold model: `prediction = (w1 * f1 + w2 * f2 > 0) ? 1 : 0`.
   - Perform a grid search over integers `w1` in `[-10, 10]` and `w2` in `[-10, 10]`.
   - Evaluate each `(w1, w2)` pair using 2-Fold Cross-Validation:
     - Split the cleaned dataset into two folds: Fold A (even indices in the cleaned dataset: 0, 2, 4...) and Fold B (odd indices: 1, 3, 5...).
     - Compute accuracy (percentage of correct predictions) of the weights on Fold B (using only instances in Fold B). Wait, to clarify: for a fixed `(w1, w2)`, the accuracy on Fold A is `accA`, and on Fold B is `accB`.
     - Since there is no actual "training" algorithm (we are just doing a grid search for weights), the cross-validation score for a given `(w1, w2)` pair is simply the average of its accuracy on Fold A and its accuracy on Fold B: `CV_Score = (accA + accB) / 2.0`.
   - Find the `(w1, w2)` pair that maximizes the `CV_Score`.
   - If there is a tie in `CV_Score`, choose the pair with the largest `w1`. If still tied, choose the largest `w2`.

4. **Experiment Artifact Logging**:
   - Write the results to a JSON file at `/home/user/artifact.json`.
   - The format must be exactly:
     `{"best_w1": W1, "best_w2": W2, "cv_score": SCORE}`
   - Format `SCORE` to exactly 4 decimal places.

Compile and run your C program to generate the `/home/user/artifact.json` file. Ensure your C program includes all necessary headers and can be compiled with `gcc /home/user/train.c -o /home/user/train -lm`.