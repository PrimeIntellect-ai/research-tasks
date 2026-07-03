You are a data engineer building a new Graph API to analyze financial transaction networks. 

We have a legacy relational datastore exposed via an HTTP service, but it is too slow for complex network queries. Your task is to build an ETL pipeline that pulls this data, models it as a graph, and serves it via a new API.

The legacy system is located in `/app/legacy_system/`. Start it by running:
`python /app/legacy_system/server.py`
This service will bind to `127.0.0.1:5000`.

**Step 1: Reverse Engineer & Extract**
The legacy API on `127.0.0.1:5000` has the following undocumented endpoints:
- `/api/entities`
- `/api/accounts`
- `/api/transactions`
You must query these endpoints, reverse-engineer their relational data model (inferring how entities relate to accounts, and how transactions link accounts), and extract all the records.

**Step 2: Build the Graph & Serve**
Write a Python HTTP web service (using Flask, FastAPI, or standard library) that listens on `127.0.0.1:8080`. 
Your service must construct an in-memory graph from the extracted data (you may use `networkx` or standard dictionaries) where:
- Nodes can be either `Entity` or `Account`.
- Edges represent ownership (Entity <-> Account) or fund transfers (Account -> Account).

Your service on `127.0.0.1:8080` must expose the following HTTP GET endpoints:

1. `/shortest_path`
   - **Query Params:** `src_entity` (string), `dst_entity` (string).
   - **Returns:** JSON object `{"path": ["E_1", "A_5", "A_9", "E_2"]}` representing the shortest path of IDs (Entities and Accounts) between the two entities. Return `{"path": []}` if no path exists. All edge traversals are treated as undirected for the shortest path.

2. `/exposure`
   - **Query Params:** `entity_id` (string), `limit` (int), `offset` (int).
   - **Returns:** JSON object `{"accounts": [...]}`. 
   - **Logic:** Find all *Accounts* that are exactly 1 transaction hop away from any account owned by `entity_id`. Calculate the total transaction volume (sum of amounts, both in and out) between the entity's accounts and these 1-hop accounts. Return a list of the 1-hop account IDs, sorted descending by this total volume, then alphabetically by account ID. Apply the `limit` and `offset` to this sorted list for pagination.

Keep your service running in the background or foreground so that the automated verifier can query `127.0.0.1:8080`. Ensure you write clean code and validate your schema internally.