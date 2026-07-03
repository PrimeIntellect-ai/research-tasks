You are an MLOps engineer tracking experiment artifacts. 

We have a machine learning pipeline script located at `/home/user/experiment.py` that reads a dataset from `/home/user/data.csv`. The script performs schema enforcement, hyperparameter tuning using cross-validation, and saves artifacts (`results.png` and `best_score.txt`).

However, there are two issues with the current pipeline:
1. **Numerical Accuracy / Schema Bug:** The schema enforcement prematurely casts the target variable `y` to an integer, losing precision and reducing the accuracy of the model's evaluation.
2. **Artifact Tracking Bug:** The generated plot `results.png` is completely blank due to a matplotlib misconfiguration or incorrect function ordering in the script.

Your task:
1. Fix `/home/user/experiment.py` so that the target variable `y` is properly treated as a `float` during schema enforcement.
2. Fix the matplotlib code in `/home/user/experiment.py` so that `results.png` successfully saves the plot (it should not be an empty or blank image).
3. Run the script to generate the corrected `/home/user/best_score.txt` and `/home/user/results.png`.

The script should run without errors and output the best cross-validation score (Negative Mean Squared Error, flipped to positive) to `best_score.txt` formatted to 4 decimal places.