You are assisting a data researcher in organizing a large collection of machine learning datasets. The researcher has set up two local microservices in `/app/` to help manage the data, but needs a highly performant C++ service to tie them together and perform similarity-based recommendations.

Here is the environment you are working with:
1. **Metadata Service**: Runs on `127.0.0.1:8080`. 
   - `GET /datasets` returns a JSON array of datasets: `[{"id": "ds1", "description": "Global weather patterns..."}, ...]`
2. **Embedding Service**: Runs on `127.0.0.1:8081`. 
   - `POST /embed` accepts `{"text": "some text"}` and returns a JSON object with a normalized vector: `{"embedding": [0.1, 0.5, ...]}`.

Your task is to implement a C++ service that acts as the primary Similarity Search and Recommendation engine.

**Step 1: Setup & Dependencies**
- You do not have `sudo` access, but `libcurl4-openssl-dev` is installed. 
- Create a directory `/home/user/include`.
- Download `httplib.h` (cpp-httplib) and `json.hpp` (nlohmann/json) into `/home/user/include` to use for your HTTP server and JSON parsing.

**Step 2: C++ Application**
Write a C++ application at `/home/user/recommender.cpp` that does the following on startup:
1. Fetches all dataset metadata from the Metadata Service (`GET /datasets`).
2. Iterates over every dataset and fetches the embedding for its `description` from the Embedding Service (`POST /embed`).
3. Stores the joined data (IDs and their corresponding embeddings) in memory.
4. Starts an HTTP server listening on `127.0.0.1:9000`.

**Step 3: Recommendation Endpoint**
Your C++ server must expose a single endpoint: `GET /search?q=<query_text>&k=<number>`
When this endpoint is hit, it must:
1. Start a high-resolution timer.
2. Fetch the embedding for `<query_text>` from the Embedding Service.
3. Compute the cosine similarity between the query embedding and all dataset embeddings in memory.
4. Sort the datasets by highest similarity score.
5. Stop the timer and compute the elapsed time in milliseconds.
6. Append a benchmark log to `/home/user/benchmark.log` exactly in this format: `[<query_text>] time_ms: <float>`
7. Return a JSON response with the top `k` results in the following format:
   `{"results": [{"id": "ds_x", "score": 0.952}, {"id": "ds_y", "score": 0.811}]}` (Scores should be floats).

**Execution:**
- Start the backend services by running `/app/start_services.sh &`.
- Compile your C++ code (make sure to link `-lcurl` and include your headers).
- Run your C++ service in the background and leave it listening on port `9000`.