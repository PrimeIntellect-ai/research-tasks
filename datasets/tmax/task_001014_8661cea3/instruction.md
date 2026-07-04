You are a data engineer tasked with building an ETL pipeline that processes spoken infrastructure dependency reports.

We have received an audio recording from the network architecture team detailing the topology of our new microservices cluster. The recording dictates directed dependencies (e.g., "Service Alpha calls Service Beta").

Your objective is to:
1. Transcribe the audio file located at `/app/network_topology.wav`. You may use tools like `whisper.cpp` (you'll need to clone and build it) or any other local transcription utility.
2. Write a Go program at `/home/user/etl.go` that:
   - Reads the generated transcript.
   - Parses the text to extract the directed dependencies (assume a format similar to "[Source] calls [Target]").
   - Initializes a local SQLite database (`/home/user/topology.db`) and creates a table for these edges.
   - Inserts the parsed edges into the database.
   - Uses a recursive SQL query (Recursive CTE) to calculate the "total downstream impact" for every service. The total downstream impact is defined as the total number of unique services that can be reached recursively starting from a given service (excluding itself).
   - Exports the final impact scores to a JSON file at `/home/user/impact.json` in the format: `{"ServiceName": integer_count}`.

Constraints & Requirements:
- The Go program must handle database creation and the recursive aggregation query.
- Use `github.com/mattn/go-sqlite3` for the SQLite driver.
- Due to potential transcription inaccuracies, your parsing logic should be robust.
- The automated verification will compare your `impact.json` against the ground truth using a Mean Absolute Error (MAE) metric. You must achieve an MAE of 1.5 or lower.