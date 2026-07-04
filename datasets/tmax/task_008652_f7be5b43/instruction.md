You are an MLOps engineer tasked with analyzing experiment artifacts to predict model performance. 

You have been given a tar archive of experiment logs located at `/home/user/logs.tar.gz`. Each log file inside the archive contains metadata from a past training run, formatted with key-value pairs. Specifically, they contain `learning_rate`, `batch_size`, and the resulting `validation_accuracy`.

Your task is to write a bash script at `/home/user/predict.sh` that takes two arguments: a new `learning_rate` and a `batch_size`, in that order. 

When executed, your script must:
1. Extract the logs from `/home/user/logs.tar.gz`.
2. Parse the files to build a dataset of `learning_rate` and `batch_size` (as features) and `validation_accuracy` (as the target).
3. Train a Linear Regression model (you may use an inline Python script with `scikit-learn` or `numpy` within your bash script) on this dataset.
4. Print the predicted `validation_accuracy` for the provided arguments to standard output, rounded to exactly 4 decimal places.

Example execution:
```bash
$ bash /home/user/predict.sh 0.03 64
0.8660
```

Make sure your script does not print anything else to standard output besides the final 4-decimal number.