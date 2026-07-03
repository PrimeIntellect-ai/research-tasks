You are an MLOps engineer reviewing a C++ pipeline that performs simple dimensionality reduction (mean centering and 1D projection) followed by a Naive Bayes classification. 

Our experiment tracking system flagged this pipeline for suspiciously high accuracy on the test set. We suspect there is a classic data leakage issue: the pipeline is calculating its empirical statistics (mean) over the entire dataset before splitting it, effectively leaking information from the test set into the training phase (similar to calling `fit_transform` on the whole dataset instead of just `fit` on train and `transform` on train/test).

Your environment is set up in `/home/user/mlops_exp`. Inside, you will find:
- `data.csv`: The dataset containing 100 rows of features and labels.
- `pca_bayes.cpp`: The C++ source code for the pipeline. It reads the CSV, normalizes the data by subtracting the mean, projects it, trains a basic Bayesian classifier on the first 80 rows, and evaluates it on the remaining 20 rows.

Your task:
1. Analyze `/home/user/mlops_exp/pca_bayes.cpp` and identify the data leak.
2. Fix the C++ code to enforce proper data separation (the mean should be calculated *only* using the training data, rows 0 to 79).
3. Compile the fixed C++ code using `g++ -O3 pca_bayes.cpp -o pca_bayes`.
4. Run the compiled binary. It will print the test accuracy as a single floating-point number.
5. Save exactly this output (the single number) to a file named `/home/user/fixed_metrics.txt`.

Ensure your fix only changes the loop boundaries or calculation denominators relevant to the mean calculation to strictly use the `train_size`. Do not alter the classification logic or the random seed/data loading sections.