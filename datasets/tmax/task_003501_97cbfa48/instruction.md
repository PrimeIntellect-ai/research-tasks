We have a local build artifact proxy (`/home/user/app/proxy/main.cpp`) written in C++ that sits in front of a slow remote artifact server (`/home/user/app/backend/server.py`). 

Currently, our proxy is very naive: it just forwards requests to the remote server. The remote server is slow and strictly rate-limits us to 5 requests per second. Additionally, to save bandwidth, the remote server does not always serve full artifacts. If you request version N of an artifact, it might return a base artifact (version 0) and a series of numerical patches (diffs). 

As a build engineer, I need you to rewrite the C++ proxy to achieve high throughput and bypass the remote rate limits by efficiently caching and reconstructing artifacts locally.

Specifically, you need to:
1. **Custom Data Structure & Request Validation**: Implement a custom caching tree to store base artifacts and diffs. The tree should represent the artifact dependency graph. 
2. **Diff and Patch Processing**: When a client requests an artifact version via `GET /artifact/<id>`, your proxy must query the remote server for metadata (`GET /metadata/<id>`), which returns its parent ID (if any). If the artifact is a diff, the remote server `GET /download/<id>` returns a JSON array of integers representing the diff. You must reconstruct the requested artifact by applying the diff to the parent artifact (the reconstructed artifact is just an array of integers where `artifact[i] = parent[i] + diff[i]`).
3. **Numerical Algorithm**: Implement a simple checksum validation. Before returning a reconstructed artifact, calculate the sum of all its integers modulo 256. If it doesn't match the checksum provided in the metadata `checksum` field, drop the artifact.
4. **Rate Limiting Handling**: Your proxy must never exceed 5 requests/second to the backend. Use a test fixture and mock (or just run the provided `server.py`) to verify your implementation locally.

The backend is running on `http://127.0.0.1:8081`. Your proxy must listen on `http://127.0.0.1:8080`.
The project uses CMake and requires `cpp-httplib` and `nlohmann/json`, which are installed. You can build the proxy in `/home/user/app/proxy/build`.

After implementing, ensure both the backend and your proxy are running. 
Run the benchmark script `/home/user/app/tester/benchmark.py`. This script will blast your proxy with 10,000 requests. 

Your goal is to successfully serve the requests with a throughput of at least 500 requests per second without being blocked by the backend rate limiter. The script will output the throughput to stdout.