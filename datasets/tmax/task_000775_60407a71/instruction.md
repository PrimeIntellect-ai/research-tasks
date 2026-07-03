You are tasked with fixing and completing a C++ data cleaning pipeline. 

We have a multi-service setup located in `/app/`. When you run `/app/startup.sh`, it will start:
1. A Redis server on port 6379, pre-populated with a list of raw text snippets under the key `raw_dataset`.
2. A Python validation service on port 8080 (`http://localhost:8080/validate`).

Currently, the C++ processing worker (`/home/user/cleaner.cpp`) is meant to read from Redis, clean and deduplicate the data, enforce a strict JSON schema, and validate it against the Python service before saving it. However, it's currently producing an empty output file (similar to a graphics script generating blank plots due to a backend misconfiguration). 

Your goals are to modify `/home/user/cleaner.cpp` to fulfill these requirements:
1. **Fetch Data:** Pop all items from the Redis list `raw_dataset` (using `LPOP` or similar until empty). Each item is a JSON string: `{"id": <int>, "text": "<string>"}`.
2. **Tokenization:** For each item, extract the `text` field. Tokenize it by converting to lowercase and splitting by whitespace. Remove any punctuation from the tokens.
3. **Similarity Search (Deduplication):** Maintain a history of accepted records. Compute the Jaccard similarity between the current item's tokens and all previously accepted items. If the similarity is `>= 0.75` with *any* accepted item, discard the current item as a duplicate. (Jaccard similarity = intersection size / union size).
4. **Data Schema Enforcement & Validation:** If the item is kept, format it into a new JSON string exactly like this: `{"id": <int>, "tokens": ["<token1>", "<token2>", ...]}`. 
5. **Fix the Misconfiguration:** Send a POST request with this JSON to `http://localhost:8080/validate`. Currently, the validation service rejects all payloads because the C++ code is missing the correct `Content-Type: application/json` header, leading to silently dropped records. Fix the `cpp-httplib` request in the code.
6. **Save Output:** If the validation service returns an HTTP 200 OK, append the JSON string to `/home/user/cleaned_dataset.jsonl` (one JSON object per line).

You will need to compile the C++ code yourself. The system has `libhiredis-dev`, `nlohmann-json3-dev`, and `libcurl4-openssl-dev` / `cpp-httplib` installed.
Compile command hint: `g++ -std=c++17 -O3 cleaner.cpp -lhiredis -lpthread -o cleaner`

Run your fixed pipeline. Your final output must be located at `/home/user/cleaned_dataset.jsonl`. We will evaluate the quality of your deduplication and schema enforcement by comparing the `id`s and tokens in your output against a hidden reference dataset.