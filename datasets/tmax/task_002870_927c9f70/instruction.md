You are an AI assistant helping a data researcher organize and analyze a multimodal dataset.

The researcher has collected paired experimental data. One set of measurements was recorded via voice dictation into an audio file, and the other set was automatically logged into a CSV file.

Your objective is to:
1. Extract the numerical data from the audio recording.
2. Align it with the CSV data.
3. Compute the statistical relationship between the two.
4. Serve the results via a secure local web service for the researcher's automated data ingestion pipeline.

Here are the specific requirements:

**Data Sources:**
- **Audio Data:** Located at `/app/measurements.wav`. This file contains a spoken sequence of five integers in English (e.g., "fifty one, fifty two..."). You need to transcribe this audio and extract the 5 integers in the exact order they are spoken. You may install any standard Python packages (e.g., `SpeechRecognition`, `pocketsphinx`, or `openai-whisper` if applicable) to transcribe the audio. 
- **CSV Data:** Located at `/app/reference_data.csv`. It contains two columns: `id` and `reference_value`. There are 5 rows of data. 

**Statistical Analysis:**
Treat the audio sequence as Variable A (ordered 1 to 5) and the CSV `reference_value`s as Variable B (ordered by `id` 1 to 5).
Calculate:
1. The **Pearson correlation coefficient** between A and B.
2. The **Sample Covariance Matrix** between A and B (a 2x2 matrix). 

**Web Service Requirements:**
The researcher's ingestion script requires you to serve these metrics over HTTP.
- Create and run an HTTP server listening precisely on `127.0.0.1:9090`.
- It must expose a `GET` endpoint at `/api/analysis`.
- The endpoint must be secured. It should only return HTTP 200 and the JSON payload if the incoming request includes the HTTP header `X-Researcher-Token: alpha-bravo-charlie`. Otherwise, it should return a 401 or 403 status code.
- The successful response body must be exactly in this JSON format (with numbers rounded to exactly 4 decimal places):
  ```json
  {
    "pearson_corr": 0.9876,
    "cov_matrix": [
      [10.1234, 12.3456],
      [12.3456, 15.6789]
    ]
  }
  ```
  *(Note: The matrix should represent [[Var(A), Cov(A,B)], [Cov(B,A), Var(B)]], using sample variance/covariance (N-1 degrees of freedom).)*

Leave your server running (you can run it in the background or simply leave it running in the active terminal) so the automated verification test can query it.