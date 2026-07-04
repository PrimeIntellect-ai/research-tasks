You are a Data Analyst investigating a series of transaction deadlocks in our backend ordering system. We have exported recent lock-acquisition events to a CSV file, and the Lead Database Administrator left an audio note with critical parameters for your investigation.

Your objective is to ingest the data into a local NoSQL database, use an aggregation pipeline to identify the deadlock cycle, and expose your findings via a secured Python HTTP API.

### Files Provided
- `/app/dba_notes.wav`: An audio recording from the Lead DBA. You will need to transcribe this to extract two pieces of information:
  1. The exact **User ID** that triggered the deadlock investigation.
  2. The **Auth Token** to be used for securing your API.
- `/app/transactions.csv`: A CSV file containing transaction lock events. The columns are `tx_id`, `user_id`, `resource_id`, `lock_type` (either `REQUESTED` or `GRANTED`), and `timestamp`.

### Instructions

**Step 1: Audio Processing**
Extract the Target User ID and the secret Auth Token from `/app/dba_notes.wav`.

**Step 2: NoSQL Database Setup & Data Ingestion**
Start a local MongoDB server in user-space (e.g., using `mongod --dbpath /tmp/mongo_data --port 27017`). 
Write a Python script to parse `/app/transactions.csv` and insert the records into a MongoDB database named `deadlock_db`, in a collection named `locks`.

**Step 3: Aggregation Pipeline**
Using `pymongo`, write a NoSQL aggregation pipeline that identifies the deadlock cycle involving the Target User ID. A deadlock cycle occurs when two different users concurrently request resources that the other user has already been granted, resulting in an infinite wait (e.g., User A holds RES-1 and requests RES-2; User B holds RES-2 and requests RES-1).
Identify:
- The other user involved in the deadlock (`deadlocked_with_user`).
- The two resources involved (`resources_involved`, sorted alphabetically).

**Step 4: Result Processing API**
Write and start a Python HTTP API (using Flask or FastAPI) that serves the result of your analysis.
- **Listen Address:** `127.0.0.1:8080`
- **Endpoint:** `GET /deadlock-analysis`
- **Authentication:** The endpoint must strictly require an HTTP `Authorization` header in the format `Bearer <AUTH_TOKEN>` using the exact token extracted from the audio file. Return `401 Unauthorized` if missing or incorrect.
- **Output Schema Validation:** The endpoint must return a JSON response matching the following strict structure:
  ```json
  {
    "target_user": "<Target User ID from audio>",
    "deadlocked_with_user": "<Other User ID found via aggregation>",
    "resources_involved": ["<Resource 1>", "<Resource 2>"]
  }
  ```

Leave the API running in the background so it can be verified by our automated tests. Ensure all your dependencies (like `pymongo`, `fastapi`, `uvicorn`, transcription tools) are installed in your user environment.