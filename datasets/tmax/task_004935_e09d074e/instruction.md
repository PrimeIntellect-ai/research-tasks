You are an incoming data scientist joining a project that predicts customer purchasing behavior.

Your predecessor left a data preparation script at `/home/user/prepare_data.py`. The script joins user demographic data (`/home/user/users.csv`) with transaction data (`/home/user/purchases.csv`) and scales the features. 

However, during a code review, you noticed a critical **data leak**: the script applies `StandardScaler().fit_transform()` to the `amount` feature on the *entire* dataset before performing the train/test split. This leaks information from the test set into the training set.

Your task is to fix `/home/user/prepare_data.py` so that:
1. The data joining and NaN filling remain unchanged.
2. The `train_test_split` (with `test_size=0.2`, `random_state=42`) happens *before* any scaling.
3. The `StandardScaler` is fitted **only** on the training set.
4. Both the training and test sets are transformed using this fitted scaler.
5. The script calculates the mean of the scaled `amount` column in the **test set** and writes this single numeric value to a new file `/home/user/fixed_mean.txt`, rounded to exactly 4 decimal places.

Run your fixed script to generate the output file. You have full permission to modify `/home/user/prepare_data.py` or create new scripts to accomplish this. Standard libraries like `pandas` and `scikit-learn` are installed in the environment.