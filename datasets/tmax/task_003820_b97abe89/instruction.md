You are a database reliability engineer managing a complex graph of incremental database backups. A critical issue has occurred, and an automated system has left an audio alert detailing which backup node needs immediate auditing. 

Your task is to build a C++ microservice that processes the backup graph and serves the required audit trail.

1. **Identify the Target:**
   Extract the target backup ID from the audio voicemail located at `/app/alert.wav`. You may use Python libraries like `SpeechRecognition` or standard CLI tools to transcribe it. The ID will be mentioned phonetically (e.g., "node alpha seven" -> `A-7`).

2. **Graph Processing (C++):**
   You have a JSON file at `/home/user/backups.json` representing a graph of backup snapshots. Each object has `id`, `parent_id` (which it incrementally builds upon), `timestamp`, and `status`.
   Write a C++ program that:
   - Reads and parses the JSON file. 
   - Performs a recursive hierarchical query to find the target backup ID (from the audio) and **all** of its descendants in the backup tree.
   - Filters out any backups where `status` is not `"SUCCESS"`.
   - Sorts the resulting backups by `timestamp` in descending order.

3. **HTTP API Service:**
   The C++ program must act as an HTTP server listening strictly on `127.0.0.1:8080`.
   - Single endpoint: `GET /audit`
   - Must support query parameters `page` (1-indexed) and `limit` for pagination of the sorted descendants.
   - The output must strictly validate against this JSON schema format:
     `{"data": [{"id": string, "timestamp": number}], "total_descendants": number, "page": number}`

To help you with C++, the single-header libraries `httplib.h` (cpp-httplib) and `json.hpp` (nlohmann/json) are already placed in `/home/user/`.

Compile your server (e.g., `g++ -std=c++17 server.cpp -lpthread -o server`), start it in the background, and verify it works. Ensure the server keeps running so the automated verifier can test it.