You are a machine learning engineer working on a text classification project. Your colleague has written a script to train a model, but they suspect it might be reporting artificially high accuracy due to a data leak, and they haven't set up the code for production deployment.

You are provided with a script `/home/user/train_model.py` and a dataset `/home/user/data.csv`.

Your tasks are:
1. **Fix the Data Leak:** The current script applies a TF-IDF transformation to the entire dataset *before* splitting it into train and test sets. Modify the code so that the vectorizer is only fitted on the training data.
2. **Implement a Scikit-Learn Pipeline:** Refactor the modeling process to use `sklearn.pipeline.Pipeline` combining the `TfidfVectorizer` and `LogisticRegression`. This ensures reproducibility and prevents future leaks.
3. **Reproducible Splitting:** Keep the `train_test_split` with `test_size=0.2` and `random_state=42`. Apply it directly to the raw text and labels before the pipeline. Ensure the LogisticRegression also uses `random_state=42`.
4. **Inference Benchmarking:** After training the pipeline, benchmark its inference speed on the test set. Run `pipeline.predict(X_test)` 100 times in a loop. Calculate the average execution time per run in milliseconds.
5. **Output Metrics:** Save the final metrics to a JSON file at `/home/user/metrics.json` with the following exact keys:
   - `"test_accuracy"`: (float) The accuracy score of the pipeline on the test set.
   - `"avg_inference_ms"`: (float) The average time taken for a single `predict` call on the full test set, in milliseconds, averaged over 100 runs.
   - `"pipeline_steps"`: (list of strings) The names of the steps in your scikit-learn pipeline (e.g., `["tfidf", "clf"]`).

Ensure your resulting script `/home/user/train_model.py` is fully functional and successfully generates `/home/user/metrics.json` when run. You can install any necessary Python packages, though standard `scikit-learn` and `pandas` will suffice.