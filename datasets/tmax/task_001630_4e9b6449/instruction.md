You are an AI assistant helping a data researcher organize and model a dataset.

The researcher has a split dataset located at:
- `/home/user/data/sensors_a.csv` (contains `id`, `sensor1`, `sensor2`)
- `/home/user/data/sensors_b.csv` (contains `id`, `sensor3`, `sensor4`)

Unfortunately, the labels for this dataset were lost. However, there is an old compiled executable at `/app/legacy_scorer` that was used to generate the labels. It takes four arguments (sensor1, sensor2, sensor3, sensor4) and outputs the predicted label (0 or 1). For example: `/app/legacy_scorer 1.2 3.4 0.1 5.5`.

The researcher wrote a preliminary script `/home/user/baseline.py` to join the data, handle missing values, query the scorer for labels, and train a model. However, they suspect the script has a data leakage issue (e.g., calling `fit_transform` on the entire dataset before splitting) making its validation score artificially high, and it struggles with outliers present in `sensors_b.csv`.

Your task:
1. Join the two datasets on `id`.
2. Perform exploratory analysis to identify and handle missing values and extreme outliers in the sensor data without introducing data leakage. 
3. Obtain labels for the training data using `/app/legacy_scorer`. You may query it as a black-box, or analyze the binary to reverse-engineer its internal logic.
4. Train a robust classification model.
5. Create a final prediction script at `/home/user/predict.py`.

The `predict.py` script must:
- Accept exactly one command-line argument: the path to an input CSV file containing `id`, `sensor1`, `sensor2`, `sensor3`, `sensor4` (some values may be missing, requiring your script to handle them as it did in training).
- Output a CSV file named `predictions.csv` in the current working directory with exactly two columns: `id` and `label` (the predicted integer class 0 or 1).

We will run your `predict.py` on a hidden test set to evaluate its accuracy.