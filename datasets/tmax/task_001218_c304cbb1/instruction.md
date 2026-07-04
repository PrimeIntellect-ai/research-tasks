I need you to build a complete end-to-end Machine Learning ETL pipeline and prediction API. 

We have a raw dataset located at `/app/raw_housing_data.csv`. However, the data dictionary that explains how to preprocess specific engineered features was only given to us as an image, located at `/app/scaling_rules.png`.

Your objectives:
1. **Extract Rules**: Use OCR to extract the transformation rules from `/app/scaling_rules.png`. It contains a specific mathematical formula for scaling the `Area` and `Age` columns.
2. **Build the ETL & Train Model**: 
   - Load `/app/raw_housing_data.csv`.
   - Apply the scaling rules extracted from the image to the `Area` and `Age` columns.
   - Note: Be extremely careful not to leak information between your training and testing sets. Any data-dependent scalers (like standardization) must be fit ONLY on the training data, but applied to both. The image contains a fixed linear transformation, but you must also standardize the `Income` column using z-score normalization.
   - Train a simple Linear Regression model to predict the `Price` column. You must use an 80/20 train/test split.
3. **Deploy Prediction API**:
   - Create a web service listening on `127.0.0.1:5000` over HTTP.
   - The service must expose a POST endpoint at `/predict`.
   - The endpoint will receive a JSON payload like: `{"Area": 1500, "Age": 10, "Income": 60000}`.
   - The API must apply the exact same ETL transformations (including the fixed scaling from the image and the z-score normalization using the parameters learned from the training set) and return the prediction as JSON: `{"predicted_price": 450000.5}`.

Requirements:
- You must save the final trained model parameters and the ETL state (e.g., mean/std from `Income`) so the API can use them.
- Ensure the API returns a 200 OK status code with the JSON response.
- Start the server in the background so it remains running. Write the PID of the server to `/app/api.pid`.

Do not use root access. You may use any language, but Python (Flask/FastAPI + scikit-learn/pandas) is recommended.