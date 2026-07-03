You are assisting a researcher who is organizing a large dataset of academic papers and their citation network. 

We have provided a SQLite database at `/app/research.db` containing two tables:
- `papers(id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)`
- `citations(source_id INTEGER, target_id INTEGER)` representing a directed edge from the citing paper (`source_id`) to the cited paper (`target_id`).

However, the database is suffering from a corrupted index on the `citations` table. The index currently returns stale, phantom rows when queried, which skews citation counts. Your first step should be to repair the database (for example, by rebuilding the indexes or dropping the corrupted ones) before serving the data.

Additionally, you have been provided with an audio file at `/app/instructions.wav`. The researcher has dictated the secret authentication passphrase into this file. You must transcribe it to retrieve the passphrase.

Your objective is to build and run an HTTP API server listening on `127.0.0.1:8080` that serves analytical graph queries over the dataset.

**API Requirements:**
1. **Authentication:** All endpoints must require an `Authorization` header in the format:
   `Authorization: Bearer <PASSPHRASE_FROM_AUDIO>`
   Requests without this header or with the wrong passphrase must return an HTTP 401 Unauthorized status.

2. **Endpoint 1: `GET /api/hindex?author=<Author Name>`**
   Calculates the h-index of the specified author. The h-index is defined as the maximum value $h$ such that the given author has published at least $h$ papers that have each been cited at least $h$ times.
   - Example Request: `GET /api/hindex?author=Alice+Smith`
   - Response Format (JSON): `{"author": "Alice Smith", "h_index": 4}`
   *(Note: You are highly encouraged to use SQL Window Functions to compute this efficiently).*

3. **Endpoint 2: `GET /api/top_papers`**
   Returns the top 5 most cited papers in the entire dataset, sorted in descending order by citation count.
   - Response Format (JSON): 
     ```json
     [
       {"title": "Graph Neural Networks", "citation_count": 150},
       ...
     ]
     ```

You may use Python (e.g., Flask, FastAPI, standard library), Node.js, or any other language of your choice to implement the API. Keep the server running in the foreground or background so that our automated test suite can verify the endpoints.