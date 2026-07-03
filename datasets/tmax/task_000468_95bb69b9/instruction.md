I am a researcher organizing some datasets for a machine learning pipeline. Before applying dimensionality reduction techniques like PCA, I need to mean-center my data. Since I am building a lightweight reproducible pipeline, I want to do this entirely using standard Linux command-line tools (like `awk`, `sed`, or standard bash built-ins) without relying on Python or R.

I have a dataset located at `/home/user/dataset.csv`. It contains 3 columns of comma-separated numeric data and no header row.

Please create a bash script at `/home/user/preprocess.sh` that does the following when executed:
1. Reads `/home/user/dataset.csv`.
2. Calculates the mathematical mean (average) of each of the 3 columns.
3. Mean-centers the dataset by subtracting the respective column's mean from every value in that column.
4. Saves the mean-centered dataset to `/home/user/centered_data.csv`, formatting every number to exactly 2 decimal places (e.g., `1.50`). The output must be comma-separated.
5. Implements basic experiment tracking by appending a log entry to `/home/user/metrics.log`. The log entry must exactly match this format:
   `Col1_mean=X.XX, Col2_mean=Y.YY, Col3_mean=Z.ZZ`
   (Replace X.XX, Y.YY, and Z.ZZ with the calculated means, formatted to 2 decimal places).

Ensure your script is executable (`chmod +x`) and then run it so that `centered_data.csv` and `metrics.log` are generated.