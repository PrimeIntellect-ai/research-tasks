You are a Machine Learning Engineer preparing a dataset of text embeddings for a Bayesian classification model. 

We have a dataset located at `/home/user/embeddings.csv` containing 100 rows. Each row has 3 continuous features (embedding dimensions) and 1 binary integer target class (0 or 1) in the last column.

You have been given a bash script at `/home/user/normalize.sh` that normalizes the data to a [0, 1] range using Min-Max scaling and splits it into a training set and a testing set. However, there is a critical **data leakage** bug: the script computes the minimum and maximum feature values over the *entire* dataset before splitting it.

Your tasks are:
1. Fix `/home/user/normalize.sh` so that the minimum and maximum values for each of the 3 feature columns are calculated **strictly from the training set** (the first 80 rows). 
2. Use these training set minimums and maximums to normalize all 100 rows. (Features can be >1 or <0 in the test set if they fall outside the training set range, which is expected).
3. The script must still output the first 80 normalized rows to `/home/user/train.csv` and the remaining 20 normalized rows to `/home/user/test.csv`. The output values should be formatted to 4 decimal places (e.g., `printf "%.4f"`).
4. Run your corrected `normalize.sh` to generate the new data files.
5. Finally, run the provided evaluation script via `python3 /home/user/evaluate.py`. This script will train a Gaussian Naive Bayes model on `train.csv`, evaluate it on `test.csv`, and write the numerical log-probabilities to `/home/user/test_log_probs.txt`.

Do not modify `/home/user/evaluate.py`. Make sure your modified `normalize.sh` runs successfully and produces the required files.