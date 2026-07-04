You are an MLOps engineer auditing historical experiment artifacts for data leakage and feature poisoning. 

Your task is to create a validation script `/home/user/gatekeeper.py` that acts as a data and model quality filter. It must analyze a tabular dataset, test it for multicollinearity (feature poisoning) and target leakage, and classify the dataset as clean or anomalous.

First, you will find an image artifact at `/app/experiment_spec.png`. This is a screenshot of the original experiment's configuration board. You must extract the following parameters from this image:
1. The Maximum Allowable Feature Correlation (`Max_Corr`)
2. The Minimum Allowable Mean Squared Error (`Min_MSE`)
3. The specific Model Architecture and its hyperparameters used for the baseline test.

Write `/home/user/gatekeeper.py` to accept a single argument (the path to a dataset CSV). The script must perform the following pipeline:
1. Load the CSV. The target variable is always named `target`. All other columns are numerical features.
2. Calculate the absolute Pearson correlation matrix for all features (excluding `target`). If any pair of distinct features has an absolute correlation strictly greater than the `Max_Corr` value extracted from the image, the dataset is anomalous.
3. If the correlation check passes, perform a sequential 80/20 train/test split (the first 80% of rows for training, the remaining 20% for testing).
4. Train the exact model architecture extracted from the image on the training set, and predict on the test set. Calculate the Mean Squared Error (MSE).
5. If the test MSE is strictly less than the `Min_MSE` value extracted from the image, the dataset suffers from target leakage and is anomalous.
6. The script must output EXACTLY `STATUS: REJECT` if the dataset is anomalous (fails either check), or `STATUS: ACCEPT` if it passes both checks.

Requirements:
- Install any needed OCR tools (e.g., `tesseract-ocr`, `pytesseract`) to read the image.
- Handle data transformations carefully; do not shuffle the dataset during the split.
- Ensure your script relies purely on standard terminal outputs (printing to stdout) for the final status.
- Test your script thoroughly. Automated verifiers will run your script against hidden directories of clean and poisoned datasets.