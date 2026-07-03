You are an MLOps engineer tasked with reproducing a legacy machine learning pipeline. The original code and configurations were lost, but we recovered a screenshot of the experiment tracking dashboard. 

Your objectives are:
1. **Extract Configurations**: Analyze the image located at `/app/dashboard_screenshot.png`. It contains the parameters of the successful run, including the model type, the regularization parameter (`alpha`), the specific subset of features used, and a numerical library configuration parameter.
2. **Feature Engineering (R)**: Write an R script named `/home/user/engineer.R` that reads the raw dataset at `/app/data.csv`. It must filter the dataset to include ONLY the features listed in the screenshot (plus the target variable `y`), standardize (z-score scale) those features, and output the processed dataset to `/home/user/engineered.csv`.
3. **Environment Setup**: Set the environment variable mentioned in the screenshot before running your training script to ensure reproducibility.
4. **Model Training (Python)**: Write a Python script named `/home/user/train.py` that reads `/home/user/engineered.csv`, trains the specified model from `scikit-learn` using the exact `alpha` extracted from the image, and saves the trained model as a pickle file to `/home/user/model.pkl`.

Make sure to install any necessary tools (like `tesseract-ocr` for reading the image, or packages for R/Python) to complete the task.

The system will evaluate your model by loading `/home/user/model.pkl` and calculating the Mean Squared Error (MSE) on a hidden, held-out test set generated from the same distribution. Your model must achieve an MSE below 2.5 to pass.