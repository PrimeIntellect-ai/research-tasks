You are a data engineer tasked with fixing and deploying a machine learning ETL pipeline.

We have a script at `/home/user/etl.py` that trains a Ridge regression model on some synthetic data. Unfortunately, the script contains a classic "data leakage" bug: a `StandardScaler` is fitted and applied to the entire dataset *before* the train/test split. This causes information from the test set to leak into the training process.

Your tasks are:
1. **Fix the Data Leak:** Modify `/home/user/etl.py` so that the `train_test_split` occurs first (keeping the exact same `test_size=0.2` and `random_state=42`). Then, fit the `StandardScaler` **only** on the training data, and use it to transform both the training and test sets. Ensure the script saves the updated `model.pkl` to `/home/user/model.pkl`. Run the script to generate the fixed model.

2. **Extract Authentication Token:** You have been provided an audio recording at `/app/passphrase.wav`. Transcribe the spoken words in this audio file. The passphrase is the spoken content, converted to entirely lowercase, with all punctuation removed, and words separated by a single space.

3. **Deploy the Model:** Create and run a web service (using FastAPI, Flask, or a similar Python framework) that listens on `0.0.0.0:8000`. 
   - The service must expose a `POST /predict` endpoint.
   - The endpoint must accept a JSON payload in the format: `{"features": [float, float, float, float, float]}`.
   - It should use the saved scaler and model from `/home/user/model.pkl` to scale the features and generate a prediction. The response should be JSON: `{"prediction": float}`.
   - The endpoint MUST be protected by Bearer Authentication. The expected token is the exact passphrase extracted from the audio file. Clients will send the header: `Authorization: Bearer <passphrase>`. If the token is missing or incorrect, return a 401 Unauthorized status.

Ensure your web service is left running in the background on port 8000 so that our automated test suite can send requests to it. You may install any necessary Python packages (e.g., `openai-whisper`, `fastapi`, `uvicorn`, `flask`) via `pip`.