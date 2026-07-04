You are acting as a compliance officer auditing a financial system to detect suspicious money flows. The system records transactions in a MongoDB database, and we need a Go REST API to query this data for auditing purposes. 

Your task is to implement the missing querying logic in a Go web service located at `/home/user/app/main.go`.

The environment includes multiple cooperating services:
1. A MongoDB instance running on `127.0.0.1:27017`. The database is named `compliance`, and it contains a collection named `transactions`.
   The `transactions` documents have the following structure:
   `{ "_id": ObjectId(...), "from": "ACC1", "to": "ACC2", "amount": 500.0 }`

You must complete the Go service to listen on `127.0.0.1:8080` and expose two HTTP GET endpoints:

**Endpoint 1: Reachability Analysis**
`GET /api/reachable?account=<id>`
- Must perform a graph traversal using MongoDB's NoSQL aggregation pipeline (`$graphLookup`).
- Find all distinct account IDs that can be reached from the given `account` (where `from` connects to `to`) in up to 3 hops (i.e., maxDepth: 2).
- Do not include the starting account itself in the output array unless it is reachable via a cycle.
- Return a JSON response exactly in this format: `{"reachable": ["ACC2", "ACC3"]}` (the array elements can be in any order).

**Endpoint 2: Account Volume Centrality**
`GET /api/volume?page=<p>&limit=<l>`
- Calculate the total transaction volume for each account. An account's total volume is the sum of the `amount` of all transactions where it is the `from` account, PLUS the sum of the `amount` of all transactions where it is the `to` account.
- Use a MongoDB aggregation pipeline to compute this efficiently.
- Sort the results by total volume in descending order. If volumes are equal, sort by account ID in ascending alphabetical order.
- Implement pagination using the `page` (1-indexed) and `limit` query parameters.
- Return a JSON response exactly in this format: 
  `{"data": [{"account": "ACC1", "volume": 1500.0}, {"account": "ACC2", "volume": 800.0}], "page": 1}`

Requirements:
- Ensure the Go service handles missing or invalid query parameters gracefully (return HTTP 400).
- Run your Go server in the background so it is listening on `127.0.0.1:8080` when you consider the task complete. Keep it running.
- Use the official Go driver for MongoDB (`go.mongodb.org/mongo-driver/mongo`).
- Do not write a custom Go-level graph traversal; you MUST use MongoDB's aggregation pipelines (`$graphLookup`, `$facet`, `$group`, etc.) to process the data at the database level.