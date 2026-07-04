You are an AI assistant helping a dataset researcher organize a newly recovered graph dataset. The dataset was transmitted through a legacy optical system and has been captured as a video file located at `/app/dataset_transmission.mp4`.

Your goal is to extract the data from the video, store it in a relational database, and expose a graph traversal API.

**Step 1: Extract the Dataset from the Video**
The video contains a sequence of black and white frames encoding a JSON string. 
- Extract the frames in order.
- For each frame, calculate the average grayscale pixel intensity. If the average intensity is > 128, the frame represents a binary `1`. Otherwise, it represents a `0`.
- Group the bits into bytes (8 bits per byte, Most Significant Bit first).
- Decode the resulting bytes as an ASCII string.
- The decoded string is a JSON array containing the dataset (a list of edges with source, target, and weight).

**Step 2: Database Setup**
- Reverse engineer a normalized SQLite database schema to store these graph edges efficiently.
- Create an SQLite database at `/home/user/graph.db`.
- Use parameterized SQL queries to insert all the extracted edges into the database. Ensure you enforce appropriate constraints (e.g., weights should be positive).

**Step 3: Graph Traversal API**
Create a Python web server (e.g., using Flask or FastAPI) listening on `0.0.0.0:8080`.
Implement a single endpoint with the following specifications:
- **Path:** `/shortest_path`
- **Method:** `POST`
- **Authentication:** The endpoint must require an HTTP header `Authorization: Bearer RESEARCH_TOKEN_99`. Return a 401 status code if missing or incorrect.
- **Input Schema:** The request body will be JSON: `{"start": "NodeA", "end": "NodeB"}`.
- **Output Schema:** Compute the shortest path using the weights from the database. The response must precisely match this JSON schema: `{"path": ["NodeA", "...", "NodeB"], "cost": 10}`. Return a 404 status code if no path exists.

Leave the server running in the background or foreground so that the automated test suite can interact with it.