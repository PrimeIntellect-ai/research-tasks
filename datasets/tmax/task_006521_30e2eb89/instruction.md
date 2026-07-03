You are a data scientist tasked with cleaning and analyzing a dataset of system log messages to identify anomalies. 

You have been provided a dataset at `/home/user/data/logs.csv`. This file contains a single column named `message`.

Your objective is to build a pipeline that processes the text, reduces its dimensionality, and trains an anomaly detection model. Complete the following steps using the language and libraries of your choice (Python with scikit-learn is highly recommended):

1. **Dataset Preparation & Cleaning**: 
   Read `/home/user/data/logs.csv`. Clean the `message` column by converting all text to lowercase and removing all characters except alphanumeric characters (a-z, 0-9) and spaces.
   
2. **Tokenization & Feature Extraction**:
   Convert the cleaned text into a TF-IDF matrix. Remove standard English stop words during this process.

3. **Dimensionality Reduction**:
   Apply Truncated SVD to the TF-IDF matrix to reduce the feature space to exactly 2 dimensions. 
   *(Constraint: Use a random seed/state of 42 for the SVD algorithm)*

4. **Model Training & Evaluation**:
   Train an Isolation Forest model on the 2D SVD features to detect anomalous logs.
   *(Constraint: Set the `contamination` parameter to 0.1 and `random_state` to 42)*

5. **Reporting**:
   Generate a final CSV report at `/home/user/results.csv` with exactly the following columns in order:
   - `original_message`: The original, uncleaned text from the input CSV.
   - `svd_1`: The first SVD component, rounded to 4 decimal places.
   - `svd_2`: The second SVD component, rounded to 4 decimal places.
   - `is_anomaly`: An integer flag where `1` represents an anomaly and `0` represents a normal log. (Note: Isolation Forest typically outputs `-1` for anomalies and `1` for inliers; you must map these to `1` and `0` respectively).

Ensure the final CSV includes a header row and is sorted alphabetically by the `original_message` column.