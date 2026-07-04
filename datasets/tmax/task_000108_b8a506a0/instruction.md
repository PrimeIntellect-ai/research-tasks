A junior data scientist on our team wrote a machine learning pipeline script to classify a synthetic dataset. The script applies scaling, dimensionality reduction (PCA), and trains a Logistic Regression model. However, we strongly suspect that there is a data leakage bug occurring during the feature transformation step between the training and test sets, which compromises the integrity of the evaluation.

Your task is to:
1. Review the Python script located at `/home/user/model_pipeline.py`.
2. Identify and fix the data leakage bug(s) causing improper transformation of the test set. 
3. After fixing the script, execute it. The script should be modified to write the correct test set evaluation metrics to a JSON file located at `/home/user/results.json`.

The file `/home/user/results.json` must be a valid JSON object with the following exact keys and format:
```json
{
  "accuracy": <float>,
  "roc_auc": <float>
}
```
Do not change the random seeds, model hyperparameters, or the train/test split ratio. Just fix the data leakage issue in the transformation steps and ensure the results are saved to the JSON file.