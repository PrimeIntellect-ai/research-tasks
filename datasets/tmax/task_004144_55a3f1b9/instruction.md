You are a machine learning engineer preparing training data for a Graph Neural Network (GNN) model that predicts molecular energy states. 

A proprietary, legacy Fortran tool has been compiled into a standalone stripped binary located at `/app/mol_oracle`. This binary calculates an "energy score" for a given molecular topology. You need to orchestrate a data preparation pipeline that combines topological feature extraction with this oracle, and expose it via a web service for the data loaders to consume.

Your task:
1. **Understand the Oracle:** The `/app/mol_oracle` binary reads an undirected graph from standard input and prints a single floating-point number (the energy score) to standard output. The input format is:
   - First line: Two integers `N` (number of nodes) and `M` (number of edges). Nodes are 0-indexed.
   - Next `M` lines: Two integers `u v` representing an edge.
   
2. **Implement Feature Extraction & Server (C++):** 
   Write a C++ program (`/home/user/mol_server.cpp`) that acts as an HTTP server. A single-header HTTP library is provided for you at `/app/httplib.h`.
   
   The server must listen on `127.0.0.1:8080` and expose a single HTTP POST endpoint: `/process`.
   
   The `/process` endpoint will receive a JSON payload representing a graph. Example:
   `{"nodes": 4, "edges": [[0,1], [1,2], [2,3], [3,0], [0,2]]}`
   (You may use a lightweight JSON parsing approach or write a simple parser, as the format is strictly guaranteed to follow this pattern with no nested objects or extra spaces).

   For each request, your C++ code must:
   a) Parse the graph.
   b) Use a graph algorithm to calculate the exact number of **triangles** (3-node cliques) in the graph.
   c) Programmatically execute `/app/mol_oracle`, feed it the graph in its required plaintext format via `stdin`, and read the resulting float score from `stdout`.
   d) Respond to the HTTP POST request with a JSON object containing both calculated values. Format:
      `{"triangles": <int>, "oracle_score": <float>}`

3. **Orchestrate:**
   Compile your C++ program using `g++` (e.g., `g++ -O2 -std=c++11 /home/user/mol_server.cpp -o /home/user/mol_server -lpthread`). 
   Run your server in the background so it is actively listening on `127.0.0.1:8080`.

Ensure your server remains running and properly handles multiple requests. Do not terminate the server when you finish.