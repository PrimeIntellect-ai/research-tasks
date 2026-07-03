I am a technical writer managing a complex documentation system. Our system consists of three services:
1. An Nginx web server serving static documentation (runs on port 8080).
2. A Flask search service that queries documentation metadata (runs on port 5000).
3. A Redis datastore caching search metadata (runs on port 6379).

Currently, the services are broken and not communicating properly. 
First, you need to fix the services:
- Configure Nginx (`/home/user/nginx.conf`) to proxy requests from `/search` to the Flask service on `127.0.0.1:5000`.
- Update the Flask app (`/home/user/search_app.py`) to connect to Redis on `127.0.0.1:6379` instead of its current dummy configuration.
- Ensure that making a GET request to `http://127.0.0.1:8080/search?q=test` returns a 200 OK with the JSON payload from Redis.

Second, I need you to write a Python archiving script at `/home/user/archiver.py`. This script will process our documentation access logs from `stdin` and output a custom compressed binary archive to `stdout`. 
The logs come in a multi-line text format:
```
[REQ_START] id=123
{"endpoint": "/search", "status": 200}
[REQ_END]
```

Your script must:
1. Read the stream from standard input.
2. Extract the JSON payload between `[REQ_START]` and `[REQ_END]`.
3. Convert the extracted JSON objects into a single CSV string (columns: `endpoint`, `status`, sorted by endpoint name).
4. Compress the resulting CSV string using a custom Run-Length Encoding (RLE). The RLE rule is: If any alphabetic character (a-z, A-Z) repeats 3 or more times consecutively, replace the sequence with `~<count><char>` (e.g., `aaa` becomes `~3a`, `bbbb` becomes `~4b`). Non-alphabetic characters and sequences of length < 3 are left uncompressed.
5. Write the compressed output to standard output.

We have a reference binary that perfectly implements this archiving logic. Your Python script's output must be bit-exact equivalent to our reference binary for any valid log input stream.