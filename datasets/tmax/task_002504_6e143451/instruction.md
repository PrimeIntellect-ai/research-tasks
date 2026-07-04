You are a Database Administrator tasked with optimizing and exposing infrastructure querying for our internal developer platform.

Our network topology and database dependencies are stored in a local SQLite database located at `/app/infrastructure.db`. 
We also have a voicemail memo from the Lead Architect located at `/app/architect_memo.wav`. 

Your task is to:
1. Transcribe the audio memo (`/app/architect_memo.wav`). It contains a highly sensitive, alphanumeric authorization token required for the new API you will build. You may install standard Python audio processing libraries (like `SpeechRecognition` and `pocketsphinx`, or `openai-whisper`) to decode this file.
2. Build a Python HTTP API listening strictly on `127.0.0.1:8000` (e.g., using Flask or FastAPI).
3. The API must require the exact authorization token extracted from the audio memo in the `Authorization` header as a Bearer token (e.g., `Authorization: Bearer <TOKEN>`).
4. Implement the following endpoints using parameterized queries and graph traversal logic on the SQLite database:

   a) **GET /path?source=<node_name>&target=<node_name>**
      - Compute the shortest dependency path between the `source` and `target` nodes based on the `latency` weight.
      - The database has two tables: 
        - `nodes(id INTEGER PRIMARY KEY, name TEXT)`
        - `edges(source_id INTEGER, target_id INTEGER, latency INTEGER)`
      - Return a JSON response in the format: `{"path": ["source_name", "intermediate_name", "target_name"], "total_latency": 150}`. 
      - You may extract the graph to memory (e.g., using `networkx`) or use Recursive CTEs, but ensure safe parameterized SQL queries are used.

   b) **GET /export**
      - Perform cross-query aggregation: calculate the total outgoing latency for every node in the graph.
      - Export and return this data strictly in `text/csv` format. 
      - The CSV must have exactly two headers: `node_name,total_outgoing_latency`. 
      - Order the CSV by `total_outgoing_latency` descending.

Keep the server running in the foreground or background so that our automated test suite can exercise the HTTP endpoints via actual network calls.