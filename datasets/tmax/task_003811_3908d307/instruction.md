You are tasked with modernizing a legacy data cleaning pipeline. 

Currently, our company uses a proprietary, closed-source anomaly detection engine to filter out anomalous text data. This engine is provided as a compiled Linux binary located at `/app/legacy_scorer`. Unfortunately, it is extremely slow, making it a bottleneck for our real-time inference pipeline. 

Your goal is to train a fast "student" model in Python that mimics the behavior of this slow "teacher" binary, and then write an optimized inference script.

Here is the workflow you need to execute:

1. **Environment Setup**:
   Install any Python libraries you need. You will likely need `pandas`, `scikit-learn`, and `sentence-transformers`.

2. **Data Transformation & Embedding**:
   You have a raw dataset at `/home/user/raw_data.csv` containing columns `id` and `text`.
   - Drop any rows where `text` is missing or consists entirely of whitespace.
   - Compute text embeddings for the cleaned `text` column using the `sentence-transformers/all-MiniLM-L6-v2` model.

3. **Legacy Oracle Interaction**:
   The legacy binary at `/app/legacy_scorer` takes a CSV of embeddings and outputs anomaly scores.
   - Usage: `/app/legacy_scorer <input_embeddings.csv> <output_scores.csv>`
   - The input must be a headerless CSV containing only the comma-separated embedding dimensions (384 columns for the MiniLM model) for each row.
   - The output will be a single-column headerless CSV containing a float score (between 0 and 1) for each row.
   Run your embeddings through this binary to get the target anomaly scores.

4. **Model Training (Knowledge Distillation)**:
   Train a regression model (e.g., Ridge Regression, MLP, or similar) using `scikit-learn` to predict the legacy anomaly scores directly from the embeddings. 
   Save your trained model to `/home/user/student_model.pkl` using `joblib`.

5. **Inference Benchmarking & Integration**:
   Write a final inference script at `/home/user/predict.py`.
   - The script must accept two command-line arguments: `python /home/user/predict.py <input_text_csv> <output_predictions_csv>`
   - It should read the input CSV (which will have `id` and `text` columns), compute the embeddings using `all-MiniLM-L6-v2`, and use `/home/user/student_model.pkl` to predict the anomaly scores.
   - The output must be a CSV with two columns: `id` and `score`, including headers.
   - Do NOT call the legacy binary in this script.

Your final solution will be verified against a hidden test set. The automated test will run your `/home/user/predict.py` script on the hidden data and compute the Mean Squared Error (MSE) between your student model's predictions and the true legacy binary outputs. Your model must achieve an MSE of **less than 0.01**.