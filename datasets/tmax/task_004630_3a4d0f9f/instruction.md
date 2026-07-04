You are helping a researcher organize and debug their datasets and experiment tracking scripts. 

The researcher has written a Python script located at `/home/user/experiment.py` that tests a similarity search / classification pipeline. It loads a dataset, scales the features, and evaluates a k-Nearest Neighbors classifier. 

However, the researcher suspects there is a **data leakage** bug in the preprocessing step of the scikit-learn pipeline, specifically relating to how `fit_transform` is used before splitting the dataset. This is artificially inflating the reported accuracy because information from the test set is leaking into the training set via the scaler.

Your tasks are to:
1. Examine `/home/user/experiment.py` and identify the data leakage.
2. Fix the script so that the scaling transformation prevents data leakage (i.e., fit only on the training data, then transform both train and test data).
3. Save the corrected script to `/home/user/experiment_fixed.py`.
4. Run the fixed script and save its standard output (the corrected accuracy score, rounded to 4 decimal places) to `/home/user/fixed_metric.txt`.

Ensure any necessary packages like `scikit-learn` are installed in your environment before running the scripts. Use bash commands and Python to complete the objective.