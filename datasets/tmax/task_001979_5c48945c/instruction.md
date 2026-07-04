You are acting as a machine learning engineer tasked with preparing a training dataset and setting up a validation API.

We have a raw dataset located at `/app/raw_data.csv` containing numerical features (`alpha`, `beta`, `gamma`) and a target variable (`target`). 
Our data science lead left a screenshot of the data schema and mathematical validation rules in an image located at `/app/schema.png`.

Your task is to:
1. Extract the mathematical constraints and schema rules from the image `/app/schema.png` using OCR (tesseract is available).
2. Write a reproducible Python script that loads `/app/raw_data.csv`, applies the extracted constraints to filter out invalid rows, and saves the resulting dataset to `/app/clean_data.csv`. 
3. Build and launch a lightweight Python HTTP API (using Flask or FastAPI) listening strictly on `127.0.0.1:8080`.
4. The API must expose two endpoints:
   - `GET /stats`: Returns a JSON response exactly in this format: `{"initial_rows": <int>, "cleaned_rows": <int>}` representing the dataset sizes before and after applying the schema.
   - `GET /data`: Returns the cleaned data as a JSON list of dictionaries (records format).

Requirements:
- Ensure your data pipeline strictly enforces the mathematical schema found in the image.
- Leave the API running in the background so it can be queried. 
- Ensure your code handles data validation gracefully.