You are acting as a database administrator. We have lost the original database schema documentation. However, we have a screen recording video file located at `/app/db_recording.mp4` which contains an embedded subtitle track (stream 0:1) logging the slow queries executed on the system over time.

Your task is to:
1. Extract the subtitle stream from `/app/db_recording.mp4` to retrieve the SQL queries.
2. Reverse-engineer the database schema by analyzing these queries. Deduce the tables and their corresponding columns.
3. Write a Bash script to spin up a simple HTTP server that listens on `0.0.0.0:8080`.
4. The server must handle a `GET /api/schema` request and respond with a 200 OK HTTP status and a JSON payload representing the reverse-engineered schema.

The JSON response body must have the following format exactly (a dictionary mapping table names to sorted arrays of column names, both alphabetically sorted):
```json
{
  "table1": ["colA", "colB"],
  "table2": ["colC", "colD"]
}
```

Ensure your HTTP server script runs continuously and responds correctly to standard HTTP GET requests so that an automated verifier can test it. You can use tools like `nc`, `socat`, `jq`, `awk`, and `ffmpeg` which are available on the system.