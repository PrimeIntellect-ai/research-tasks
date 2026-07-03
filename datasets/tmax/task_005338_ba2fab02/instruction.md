You are tasked with fixing and orchestrating an end-to-end Machine Learning pipeline for a data science team.

Currently, we have three services running in a local multi-service architecture:
1. **Data API** (Flask, running on `localhost:5000`): Serves raw tabular dataset chunks.
2. **Inference API** (Flask, running on `localhost:5001`): Serves predictions using a trained model.
3. **Redis** (running on `localhost:6379`): Used for caching data.

Your workspace is in `/home/user/ml_pipeline/`. Inside, you will find:
- `train.py`: A Python script that trains a Scikit-Learn `LogisticRegression` model. It takes an argument `--C` for the regularization parameter, evaluates the model using cross-validation, and saves `model.pkl`.
- `pipeline.sh`: A Bash script meant to orchestrate the workflow.
- `serve.sh`: A script that restarts the Inference API to load the latest `model.pkl`.

**Problems you need to solve:**
1. **Data Leakage**: The `train.py` script currently suffers from a subtle data leakage bug during preprocessing (it applies `fit_transform` on the entire dataset before splitting it for validation). This causes wildly optimistic validation scores, but terrible performance in production. Fix the Python script so that the preprocessing (scaling) is strictly fitted ONLY on the training folds/splits, preventing leakage.
2. **Bash Orchestration & Hyperparameter Tuning**: Modify `pipeline.sh` to:
   - Use `curl` to download the dataset from `http://localhost:5000/download` and save it to `data.csv`.
   - Implement a hyperparameter tuning loop in **Bash**. The Bash script must iterate over the values `C = 0.01, 0.1, 1, 10, 100`.
   - For each value, call `train.py --data data.csv --C $C`.
   - Capture the output validation score from `train.py`, determine which `C` yielded the highest score, and retrain the final model using that best parameter.
   - Copy the best `model.pkl` to `/home/user/ml_pipeline/deploy/model.pkl`.
   - Execute `./serve.sh` to load the new model into the Inference API.
3. **Integration**: Ensure the Inference API successfully responds to POST requests at `http://localhost:5001/predict` containing JSON features. 

To complete the task, your deployed model must achieve an accuracy of strictly greater than **0.82** on a hidden, held-out dataset that the automated verifier will test against the Inference API. 

Run your `pipeline.sh` to generate the final model and start the inference server. Leave the Inference Server running on port 5001 when you are finished.