I am a researcher trying to organize my experimental datasets and evaluate the reliability of my predictive models. I have a dataset located at `/home/user/experiments.csv` which contains three continuous features: `temperature`, `pressure`, and `humidity`, along with a binary target variable `outcome`.

I need you to write a Python script at `/home/user/analyze.py` that calculates the 95% confidence interval of the cross-validated accuracy for a Gaussian Naive Bayes classifier using bootstrap resampling.

Here is the exact procedure the script must implement:
1. Load the dataset using pandas.
2. Perform 1000 bootstrap iterations. For each iteration `i` (from 0 to 999):
   - Generate a bootstrap sample of the dataset (sample with replacement, same size as original) using `random_state=i`.
   - On this bootstrap sample, perform 5-fold Stratified Cross-Validation using a Gaussian Naive Bayes classifier. Use `shuffle=True` and `random_state=i` for the Stratified K-Fold splitter.
   - Calculate the mean accuracy across the 5 folds for this iteration and store it.
3. After collecting all 1000 mean accuracies, compute the 2.5th and 97.5th percentiles to form the 95% confidence interval. (Use numpy's `percentile` function).
4. Save the confidence interval to a file named `/home/user/ci.txt`. The file should contain exactly one line with the lower and upper bounds formatted to three decimal places inside square brackets, separated by a comma and a space. For example: `[0.654, 0.876]`.

Please write the script, run it, and ensure `/home/user/ci.txt` is created with the correct format. Make sure to use `scikit-learn`, `pandas`, and `numpy`.