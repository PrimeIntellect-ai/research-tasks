You are an AI assistant helping a bioinformatics researcher organize a dictated dataset of protein interactions into a queryable knowledge graph. 

The researcher has recorded their lab notes in an audio file located at `/app/interactions.wav`. Your task is to transcribe this audio, extract the graph of protein interactions, and serve this data via a custom-built HTTP API using **Bash**.

**Step 1: Transcription & Extraction**
1. Transcribe the audio file `/app/interactions.wav` (you may install tools like `openai-whisper` via pip).
2. The dictated audio contains sentences describing protein interactions in the format: `[Protein1] [relation] [Protein2]`. (e.g., "ProteinA activates ProteinB"). 
3. Extract these interactions into a flat text format of your choice, ensuring you capture the source protein, the relation type, and the target protein. Ignore conversational filler like "Dataset recording begins" or "End of recording."

**Step 2: Bash-based HTTP Graph API**
Build an HTTP server that listens on `127.0.0.1:8080`. 
**Constraint:** The core logic for querying the data must be written in **Bash** using standard Unix text-processing tools (like `awk`, `grep`, `jq`, `sort`). You may use tools like `socat` or `nc` to handle the TCP/HTTP binding, but do not use Python/Node.js for the data querying logic.

The API must support the following exact endpoints:

1. **`GET /interactions?protein=<NAME>`**
   Returns a JSON array of all outgoing interactions for the specified protein. The array must be sorted alphabetically by the target protein's name.
   *Example Output:*
   ```json
   [
     {"target": "ProteinB", "relation": "activates"},
     {"target": "ProteinC", "relation": "inhibits"}
   ]
   ```
   If the protein has no outgoing interactions or does not exist, return an empty array `[]`.

2. **`GET /export`**
   Returns the entire knowledge graph as a JSON array of objects, sorted alphabetically first by source protein, then by target protein.
   *Example Output:*
   ```json
   [
     {"source": "ProteinA", "relation": "activates", "target": "ProteinB"},
     {"source": "ProteinA", "relation": "inhibits", "target": "ProteinC"}
   ]
   ```

**Requirements:**
- The HTTP responses must include valid HTTP/1.1 headers (e.g., `HTTP/1.1 200 OK` and `Content-Type: application/json`).
- Ensure your server runs in the background or is started as a persistent service so it can be queried by the verification suite.
- Once your server is up and listening on `127.0.0.1:8080`, create a file named `/app/ready.txt` containing the word `READY` to signal the testing suite to begin verification.