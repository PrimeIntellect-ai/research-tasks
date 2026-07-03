You are a data engineer building an ETL pipeline that processes, indexes, and serves semantic searches over audio recordings of customer support calls.

Your goal is to build an end-to-end pipeline that transcribes an audio file, chunks the text, computes embeddings, and serves them via an authenticated REST API.

Here are your instructions:

1. **Audio Transcription (Model Inference)**
   - You are provided with an audio file of a customer support call at `/app/data/support_call.wav`.
   - Write a Python script to transcribe this audio file using the `openai/whisper-tiny` model from the Hugging Face `transformers` library.

2. **Feature Engineering & Storage (Embedding & Indexing)**
   - Take the full transcript string and split it into chunks based on sentence boundaries. Specifically, split the text using a regular expression that splits on a period or question mark followed by a space (e.g., `(?<=[.?])\s+`). Strip any leading or trailing whitespace from each chunk and discard empty chunks.
   - Using the `sentence-transformers/all-MiniLM-L6-v2` model, compute vector embeddings for each chunk.
   - Build a FAISS index (using L2 distance, i.e., `IndexFlatL2`) and add these embeddings to the index.
   - Save the FAISS index to `/home/user/faiss_index.bin` and the ordered list of text chunks (as a JSON array of strings) to `/home/user/chunks.json`.

3. **Service Deployment (Retrieval API)**
   - Create a Python REST API using `FastAPI` (or `Flask`) that loads the saved FAISS index and chunks.
   - The server must listen on `127.0.0.1:8080`.
   - Expose a `POST /search` endpoint.
   - **Authentication:** The endpoint must strictly require an HTTP `Authorization` header containing exactly `Bearer etl-secure-token-2024`. If missing or invalid, return a `401 Unauthorized` HTTP status code.
   - **Request Format:** The endpoint should accept a JSON payload: `{"query": "<user_search_string>"}`.
   - **Logic:** Compute the embedding of the query using the same `all-MiniLM-L6-v2` model, search the FAISS index for the single closest chunk (k=1), and return the matching text chunk.
   - **Response Format:** A JSON object structured exactly like: `{"best_match": "<matched_chunk_text>"}`.

Run the server in the background so that it is actively listening on `127.0.0.1:8080` when you consider the task complete. Leave the server running.