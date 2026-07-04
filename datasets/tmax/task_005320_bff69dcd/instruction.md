You are tasked with cleaning a dataset of 10-dimensional sensor readings and replacing a legacy anomaly detection system.

Currently, we have a legacy binary located at `/app/legacy_filter`. It is a stripped binary that accepts 10 comma-separated floats (representing a single sensor reading) as a single command-line argument and prints either `clean` or `evil` to standard output. Unfortunately, this binary is far too slow and system-dependent for our new Python-based data pipeline.

Your objectives are:
1. Reverse-engineer or model the logic of the legacy binary. You can generate random 10D vectors and query `/app/legacy_filter` to create a training dataset.
2. Analyze the mathematical properties of the "clean" vs "evil" data. The underlying mechanism relies on a specific linear algebraic property and probabilistic thresholding. You will likely need to use Bayesian inference, PCA, or a linear model to capture the exact decision boundary.
3. There is a script provided at `/home/user/plot_data.py` designed to help you visualize the data distributions and track your experiment metrics. However, it currently produces blank plots or crashes due to a matplotlib backend misconfiguration. Fix this script so you can properly visualize your cross-validation and hyperparameter tuning steps.
4. Develop a highly efficient Python script at `/home/user/filter.py` that takes a path to a CSV file as its only command-line argument. The CSV file will contain 100 rows of 10 comma-separated floats (no header).
5. The script `/home/user/filter.py` must print exactly `clean` to standard output if the CSV file represents a completely clean batch, or `evil` if the CSV contains ANY anomalous ("evil") rows. 

Your script must be self-contained and utilize standard data science libraries (e.g., `numpy`, `scipy`, `scikit-learn`). It must NOT call the `/app/legacy_filter` binary. 

Ensure your `filter.py` strictly prints only "clean" or "evil" to stdout. It will be evaluated against a hidden, adversarial corpus of clean and evil CSV files to verify 100% accuracy.