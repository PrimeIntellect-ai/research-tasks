You are acting as an AI assistant for a computational researcher organizing a massive, crowdsourced biomedical literature dataset. We have a continuous ingestion pipeline where new paper records (in JSON format) are submitted by third parties. Unfortunately, some submissions are malicious (containing NoSQL injection attempts) or structurally invalid (introducing impossible citation loops). 

Our stack consists of:
1. **MongoDB (Port 27017):** Stores researcher metadata and trust metrics. Database: `biomed`, Collection: `authors`.
2. **Neo4j (Port 7687):** Stores the citation graph. Database: `neo4j`. Nodes are of label `:Paper` with property `paper_id`. Edges are `:CITES`.

Both services are pre-configured. You can start them by running the script at `/app/start_services.sh`.

Your task is to write a Python classifier at `/home/user/validate_submission.py` that takes a single JSON file path as a command-line argument and prints exactly `ACCEPT` or `REJECT` to standard output.

A submission MUST be rejected (`REJECT`) if ANY of the following criteria are met:
1. **Author Trust Failure (NoSQL Aggregation):** The JSON contains an `author_id`. You must use a MongoDB aggregation pipeline to calculate the author's average `trust_score` from their historical records in the `authors` collection. If the average `trust_score` is less than `0.5`, or if the `author_id` field in the JSON is malformed (e.g., contains NoSQL injection dictionaries instead of a string), reject it.
2. **Graph Anomaly (Cypher):** The JSON contains a `paper_id` and a list of `cites` (target paper IDs). You must query Neo4j using Cypher to check two things:
   - All target paper IDs in the `cites` list must already exist in the Neo4j database.
   - Adding this paper and its citations must not create a citation cycle of length 2 or less (i.e., you cannot cite a paper that already cites your `paper_id`).
3. **Missing Fields:** The JSON is missing `paper_id`, `author_id`, or `cites`.

If the submission passes all checks, output `ACCEPT`.

Requirements:
- Your script must be executable as: `python /home/user/validate_submission.py <path_to_json_file>`
- Print only `ACCEPT` or `REJECT` to stdout (no other text, no logging to stdout).
- You may install any Python packages you need (e.g., `pymongo`, `neo4j`).
- There are sample corpuses located at `/app/corpora/clean/` and `/app/corpora/evil/` that you can use to test your script. Your classifier must perfectly distinguish between the two.

Write the script, ensure both databases are running, and test your solution against the provided corpora.