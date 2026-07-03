You are a data engineer building an ETL pipeline that processes social network interactions. Recently, a bug in an upstream NoSQL aggregation pipeline caused an implicit cross-join, generating a massive dataset of invalid edge connections. We have reverted to the raw, uncorrupted document dump, but we need to compute key graph metrics directly from this raw NoSQL JSON export to verify our data integrity.

Your task is to write a C++ program that parses this JSON dump, builds an undirected graph, and computes the degree centrality to find the most connected node.

**Environment setup:**
- The raw NoSQL export is located at: `/home/user/raw_edges.json`
- The file contains an array of JSON objects representing directed interactions. Example:
  `[{"src": 10, "dst": 25, "interaction_type": "like"}, {"src": 25, "dst": 10, "interaction_type": "reply"}, ...]`
- A header-only JSON library for C++ is provided at `/home/user/json.hpp` (nlohmann/json).

**Requirements for the C++ program:**
1. Create your source file at `/home/user/analyze.cpp`.
2. Include the provided JSON library (`#include "json.hpp"`).
3. Read and parse `/home/user/raw_edges.json`.
4. Construct an **undirected** graph from these edges. Note: Multiple interactions between the same pair of nodes (e.g., A->B and B->A, or multiple A->B interactions) should only count as a **single unique undirected edge** when calculating the degree. 
5. Compute the degree of each node.
6. Identify the node with the highest degree. If there is a tie, select the node with the numerically smallest ID.
7. Write the result to `/home/user/result.txt` exactly in this format:
   `Max Degree Node: <node_id>, Degree: <degree>`

You must compile your program using standard `g++` (e.g., `g++ -std=c++17 -O3 /home/user/analyze.cpp -o /home/user/analyze`) and run it so that `/home/user/result.txt` is generated.