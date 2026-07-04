You are a data engineer tasked with building an automated ETL pipeline and an API service to process and serve insights from audio recordings of system logs.

There is a recording of a recent engineering status update located at `/app/audio/status_update.wav`.

Your task is to build a multi-language pipeline (using Python for data science tasks and Node.js for the API) that performs the following steps:

1. **Transcription & Tokenization (Python):**
   - Transcribe the audio file `/app/audio/status_update.wav` to text. You may use `openai-whisper` (the `tiny` model is recommended for speed) or any other offline tool you prefer.
   - Tokenize the resulting text into individual sentences.
   - Tokenize the text into lowercase words, removing basic punctuation.

2. **Bootstrapping & Statistical Analysis (Python):**
   - Perform bootstrap resampling (1,000 iterations) on the list of words to calculate the 95% confidence interval for the frequency count of the word "latency".
   - Calculate the 95% confidence interval for the frequency count of the word "database".
   - Export these statistics, the full transcript, and the list of tokenized sentences to a JSON file at `/home/user/processed_data.json`.

3. **API Service (Node.js):**
   - Create a Node.js server using Express (or standard `http` module) listening strictly on `127.0.0.1:8000`.
   - Implement the following endpoints reading from `/home/user/processed_data.json`:
     - `GET /transcript`: Returns a JSON object `{"transcript": "<full transcribed string>"}`.
     - `GET /stats`: Returns a JSON object `{"latency_ci": [lower_bound, upper_bound], "database_ci": [lower_bound, upper_bound]}` based on your bootstrap analysis.
     - `POST /search`: Accepts a JSON payload `{"query": "<search text>"}`. It should tokenize the query into words and use Jaccard similarity (intersection over union of word sets) against the tokenized sentences to find the single most similar sentence. Returns `{"match": "<most similar sentence>"}`.

**Requirements:**
- The Node.js server must be running in the background when you complete the task.
- Ensure all necessary dependencies (e.g., `express`, `openai-whisper`, `ffmpeg`) are installed in your environment.
- Start the server on port 8000 and leave it running. Ensure it binds to `127.0.0.1`.
- Do not add authentication to the endpoints.