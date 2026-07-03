You are an MLOps engineer tasked with building a reproducible artifact-tracking pipeline for a robust mathematical regression model. 

We have a dataset located at `/home/user/data/raw_data.csv` which contains three feature columns (`f1`, `f2`, `f3`) and one target column (`target`). The dataset is messy: it contains missing values in the features and extreme outliers in the target.

Your task is to create and execute a Python pipeline script at `/home/user/pipeline/train.py` that processes the data, trains a model, and saves the artifacts.

Please follow these exact specifications:

1. **Environment Setup**:
   - Create a `/home/user/pipeline/requirements.txt` containing the necessary packages (you will need `pandas`, `numpy`, `scikit-learn`).
   - Install these dependencies in the system Python environment.

2. **Data Processing**:
   - Load the CSV file.
   - **Missing Value Handling**: Impute missing values in the feature columns (`f1`, `f2`, `f3`) using K-Nearest Neighbors imputation (`KNNImputer` from scikit-learn) with `n_neighbors=3`.
   - **Outlier Handling**: Remove rows where the `target` variable is an outlier based on the Modified Z-score using the Median Absolute Deviation (MAD). 
     - The formula for the Modified Z-score is: $M_i = \frac{0.6745 \times (y_i - \tilde{y})}{\text{MAD}}$
     - Where $\tilde{y}$ is the median of $y$, and $\text{MAD} = \text{median}(|y_i - \tilde{y}|)$.
     - Remove any rows where $|M_i| > 3.5$.

3. **Model Training**:
   - Using the cleaned dataset, train a Ridge Regression model (`Ridge` from scikit-learn) with `alpha=1.0` to predict `target` from `f1`, `f2`, and `f3`.
   - Calculate the Mean Squared Error (MSE) and R-squared ($R^2$) score on the *training data itself*.

4. **Artifact Tracking**:
   - Create a directory `/home/user/artifacts`.
   - Save the trained Ridge model as a joblib serialized file at `/home/user/artifacts/model.pkl`.
   - Save the metrics as a JSON file at `/home/user/artifacts/metrics.json` with the exact keys `"mse"` and `"r2"`. Both values should be floats.

Ensure you run your pipeline script so that the artifacts are generated.