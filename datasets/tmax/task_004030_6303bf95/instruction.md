You are an MLOps engineer tasked with fixing a flawed machine learning pipeline and transitioning it to a probabilistic modeling approach.

An existing experiment script at `/home/user/experiment/pipeline.py` processes a dataset (`/home/user/experiment/data.csv`) and logs artifacts. However, the current code contains a classic data leakage issue: it applies a transformation (`StandardScaler`) to the *entire* dataset before splitting it into training and testing sets. Furthermore, the team wants to replace the current random forest model with a Bayesian inference approach for classification to better understand class probabilities.

Your objectives are:
1. **Analysis Environment Setup**: Create a Python virtual environment at `/home/user/venv`. Activate it and install `scikit-learn`, `pandas`, and `numpy`. 
2. **Fix the Data Leak**: Modify `/home/user/experiment/pipeline.py`. Restructure the code so that the dataset is split into train and test sets *first* (using `test_size=0.2, random_state=42`), and then scaling is applied correctly without leaking information from the test set into the training set. You must use `sklearn.pipeline.Pipeline` to encapsulate the scaler and the model.
3. **Probabilistic Modeling**: Replace the `RandomForestClassifier` with a Bayesian classification model: `sklearn.naive_bayes.GaussianNB`. 
4. **Numerical Accuracy & Artifacts**: The modified script should train the new pipeline, make predictions on the test set, calculate the accuracy score, and write a JSON file to `/home/user/experiment/artifacts/final_metrics.json` with the exact following format:
   ```json
   {
       "accuracy": 0.1234
   }
   ```
   (Replace `0.1234` with the actual float accuracy score).

Execute your fixed pipeline to generate the final artifacts.

Note: The directory `/home/user/experiment/artifacts/` already exists. The original `pipeline.py` and `data.csv` are in `/home/user/experiment/`.