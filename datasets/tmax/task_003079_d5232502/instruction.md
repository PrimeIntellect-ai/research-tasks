You are an AI assistant helping a researcher organize and query their datasets.

The researcher has two datasets in `/home/user/datasets/`:
1. `documents.jsonl` (JSON Lines format) - Contains `{"doc_id": "...", "title": "...", "content": "..."}`
2. `metadata.csv` - Contains `doc_id,author,timestamp_published`

The researcher was trying to use a lightweight vendored Bash HTTP server located at `/app/bashttpd-1.0` to serve this data, but it is currently broken and lacks the handler logic. 

Your task is to:
1. Fix the vendored package at `/app/bashttpd-1.0`. The script `lib/request_parser.sh` has a bug where it fails to extract URL query parameters correctly into the `QUERY_STRING` environment variable (the regex/string manipulation is currently stripping everything after the `?`). Fix this perturbation so `QUERY_STRING` contains the raw query string (e.g., `author=Smith&limit=5`).
2. Write a request handler script at `/home/user/handler.sh`. The server will source or execute this script when a request is made.
3. The handler must process a `GET /dataset` request. It should extract the `author` and `limit` query parameters from the `QUERY_STRING`.
4. Using only Bash, `jq`, `awk`, and/or `sqlite3`, the handler must dynamically join `documents.jsonl` and `metadata.csv` to find all documents written by the specified `author`.
5. The output must be returned as a valid JSON array of objects, containing `doc_id`, `title`, `author`, and `timestamp_published`. The results must be sorted by `timestamp_published` in descending order, and paginated to return a maximum number of records equal to `limit`. 
6. Start the server on port `8080` (the server script is `/app/bashttpd-1.0/server.sh --port 8080 --handler /home/user/handler.sh`) and leave it running in the background.

Make sure the HTTP server responds with standard HTTP headers (e.g., `HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n`) before the JSON payload.