You are an ML engineer tasked with preparing tabular training data and replacing a slow, legacy feature extraction pipeline.

We have a legacy proprietary feature extractor located at `/app/oracle_bin`. It is a compiled stripped Linux binary that takes exactly two float arguments (`featureA` and `featureB`) and prints a scalar float value to standard output. 

Your goals are to:
1. **Label the Training Data:** Use `/app/oracle_bin` to generate target labels for all rows in `/home/user/train.csv` by passing its `featureA` and `featureB` values to the binary.
2. **Train a Surrogate Model:** Calling a binary as a subprocess for millions of rows in production is too slow. Train a surrogate machine learning model in Python (e.g., using scikit-learn or PyTorch) on your labeled training data to approximate the oracle's outputs.
3. **Generate Predictions:** Use your trained surrogate model to predict the target values for the holdout set at `/home/user/test.csv`. Save your predictions in a CSV file exactly at `/home/user/predictions.csv` with exactly two columns: `id` and `prediction`.
4. **Fix the Visualization Pipeline:** There is a script at `/home/user/plot_data.py` designed to plot the distribution of `featureC`. Currently, running it produces an entirely blank image (`plot.png`) due to a matplotlib misconfiguration or logic error. Fix the script so it generates a correct, non-blank histogram in `plot.png`.

Your surrogate model's predictions on `test.csv` will be evaluated using Mean Squared Error (MSE) against the true outputs of the oracle. To pass, your predictions must achieve an MSE < 0.05.