You are a machine learning engineer preparing training data for a new project. A junior colleague wrote an initial script to evaluate a Logistic Regression model, but you suspect they made a critical error in their data preparation pipeline. Specifically, there is data leakage occurring between the train and test sets during feature scaling.

The script is located at `/home/user/train.py`.

Your task is to:
1. Identify the data leakage in `/home/user/train.py`.
2. Fix the Python script so that the `StandardScaler` is applied correctly without leaking test set information into the training process. 
3. Do not change any random seeds, dataset generation parameters, split ratios, or model hyperparameters.
4. Run the fixed script.

The script writes the resulting test accuracy to `/home/user/accuracy.txt`. Ensure that your final run generates this file with the correct, leakage-free accuracy. You may install any necessary Python packages.