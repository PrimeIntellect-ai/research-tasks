As a researcher organizing a massive corpus of interconnected datasets, I need to migrate our legacy graph query engine to a new high-performance C++ service. 

We have a legacy compiled query evaluator located at `/app/legacy_graph_oracle`. This is a stripped binary. It takes in a custom binary graph file (`/home/user/graph.bin`) and calculates shortest path metrics. However, we have lost the source code for the data model and the binary format parser.

Your task is to:
1. Reverse-engineer the data model expected by `/app/legacy_graph_oracle`. The binary expects a specific byte-layout for nodes, edges, and metadata (dates and access levels). 
2. Write a C++ program that reads a raw dataset log file located at `/home/user/raw_datasets.csv` and builds the optimized `graph.bin` file that the oracle can successfully read and validate (the oracle exits with code 0 if the graph structure and index are valid).
3. Build a C++ HTTP service that loads this graph. The service must listen on `127.0.0.1:8080`.
4. The service must expose a `POST /shortest-path` endpoint. It will receive a JSON payload like:
   `{"source": "DatasetA", "target": "DatasetB", "min_date": "2020-01-01", "page": 1, "limit": 10}`
5. The service must compute the shortest path between the source and target datasets, *only* traversing nodes that have a creation date >= `min_date`. 
6. The service must return an HTTP 200 JSON response containing the paginated edges of the shortest path (sorted by traversal order) and the total path cost. 
7. Ensure the service handles concurrent HTTP requests efficiently using appropriate C++ concurrency paradigms. Start your service in the background and leave it running. Write your code in `/home/user/graph_service.cpp` and compile it to `/home/user/graph_service`.

Ensure your C++ HTTP parser can handle standard `curl` POST requests. You may use standard library features (raw sockets, threads). Do not use external libraries.