As a researcher organizing datasets, I have a dataset of synthetic embeddings split into `/home/user/train.parquet` and `/home/user/test.parquet`. 

I need you to write and execute a Python script located at `/home/user/run_pipeline.py` that performs the following steps:

1. **Data Loading**: Read the training and testing datasets. The datasets contain 50 feature columns named `f0` to `f49`, and a target column named `label`.
2. **Modeling**: Train a `RandomForestClassifier` from `scikit-learn` on the training data. You MUST set `random_state=42` when initializing the classifier to ensure reproducible outputs.
3. **Inference Benchmarking**: Measure the inference performance. Run the `predict` method on the *entire test set* 10 times in a row. Compute the average time (in seconds) per full test set prediction, and write ONLY this average float value to `/home/user/inference_time.txt`.
4. **Validation**: Compute the classification accuracy on the test set and write ONLY the float value (between 0.0 and 1.0) to `/home/user/accuracy.txt`.
5. **Plotting**: Generate a confusion matrix plot for the test set predictions and save it to `/home/user/confusion_matrix.png`. 
   *Crucial Note*: The environment is a headless Linux server. You must properly configure `matplotlib` to use a non-interactive backend (such as `Agg`) *before* generating the plot to prevent crashes or blank images.

You will need to install any necessary Python packages (like `pandas`, `pyarrow`, `scikit-learn`, `matplotlib`) using `pip` before running your script.

Ensure your script runs successfully and creates `/home/user/inference_time.txt`, `/home/user/accuracy.txt`, and `/home/user/confusion_matrix.png`.