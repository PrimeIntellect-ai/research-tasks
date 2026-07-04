You are an AI assistant helping a data scientist clean and filter sensor datasets. 

We have a directory of raw CSV datasets containing sensor readings (columns `S1`, `S2`, `S3`). Some of these datasets are normal ("CLEAN"), while others contain an unacceptable amount of anomalous readings ("EVIL"). 

We have an old compiled binary tool located at `/app/legacy_detector` that detects anomalies. It reads 3 comma-separated floats from standard input (one reading per line) and outputs `1` if the reading is anomalous, and `0` if it is normal.
However, there are two problems:
1. The raw datasets contain missing values (`NaN`). The `/app/legacy_detector` binary crashes if it encounters a `NaN`.
2. The binary is too slow to run in our production pipeline, so we need a pure Python replacement.

Additionally, our data scientist left a script `/home/user/plot_posteriors.py` that was supposed to visualize the distributions of the sensor data to help build a Bayesian probabilistic model, but it is currently producing completely blank PNG files due to a matplotlib backend misconfiguration. 

Your tasks:
1. Inspect the datasets provided in `/home/user/sample_data/` and fix `/home/user/plot_posteriors.py` so it properly generates non-blank plots. 
2. Figure out the decision boundary or logic used by `/app/legacy_detector`. You can interact with the binary to reverse-engineer its logic or train a classification/regression model on its outputs.
3. Write a Python script at `/home/user/filter.py` that takes a single CSV file path as a command-line argument.
4. Your script must:
   - Read the CSV file.
   - Handle missing values (`NaN`) by imputing them using the mean of their respective column within that file.
   - Apply the anomaly detection logic (matching the legacy binary's behavior) to each row.
   - If more than 10% of the rows in the CSV are anomalous, the script must print exactly `EVIL` to standard output. Otherwise, it must print exactly `CLEAN`.

Your script `/home/user/filter.py` will be tested against a hidden, held-out corpus of clean and evil datasets. It must be robust, self-contained (do not call the legacy binary in your final script, implement the logic in Python), and correctly classify the test files.