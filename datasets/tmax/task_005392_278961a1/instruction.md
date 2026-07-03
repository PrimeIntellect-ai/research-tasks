You are assisting a compliance officer in auditing an enterprise knowledge graph for unauthorized access. We suspect an insider has been running graph queries to extract data about a highly restricted, unannounced project. 

First, we have intercepted a brief VoIP audio snippet of the suspect's conversation. The file is located at `/app/intercepted_call.wav`. Transcribe or listen to this audio (using available tools like `whisper`, `ffmpeg`, or Python libraries) to identify the specific code-name of the restricted project they mention.

Second, you need to build a query sanitizer. Employees submit graph traversal queries in JSON format. You are provided with a hierarchy of all company projects in `/app/kg_hierarchy.json` (which maps parent projects to lists of child sub-projects).

Write a Python script at `/home/user/query_filter.py` that accepts a directory path as a command-line argument. The script should:
1. Iterate through all `.json` files in the given directory.
2. Parse each JSON query. A query contains a `"start_node"` and a list of `"path"` hops (each with a `"target_node"`).
3. Reject the query if ANY node in the query's path (including the start node) is the restricted project identified from the audio, OR any of its recursive descendants (sub-projects, sub-sub-projects, etc.) based on the `/app/kg_hierarchy.json` mapping.
4. For each file, print exactly one line to standard output in the format: `filename,STATUS`, where `STATUS` is either `ACCEPT` or `REJECT`.

Your solution must be robust enough to act as a security classifier. We will test your script against two hidden corpora: one containing legitimate (clean) queries, and one containing malicious (evil) queries that attempt to access the restricted hierarchy.