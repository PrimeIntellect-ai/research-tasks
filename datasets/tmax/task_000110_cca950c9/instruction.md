You are a database administrator tasked with optimizing a NoSQL graph processing query and fixing a broken API service.

We have a multi-service application located in `/app/`. It consists of a Node.js Express API (`/app/server.js`) and a MongoDB instance running locally. The database `corp` contains a collection `employees` which models a corporate hierarchy where each document has an `_id` and an optional `managerId`.

The API has an endpoint `GET /api/subordinates` that takes query parameters `manager_id`, `page`, and `limit`. Its purpose is to return all direct and indirect subordinates for a given manager, sorted alphabetically by the employee's `name`, and paginated. 

However, the current aggregation pipeline in `/app/server.js` is broken:
1. It contains a poorly constructed `$lookup` that acts as an implicit cross join, retrieving the entire company directory instead of traversing the graph.
2. It lacks the proper query-to-pipeline chaining for sorting, skipping, and limiting the results.
3. The queries are running slowly because there is no index on the hierarchy traversal field.

Your task:
1. Modify `/app/server.js` to replace the broken `$lookup` with a correct `$graphLookup` aggregation. It should traverse the `managerId` field starting from the provided `manager_id`.
2. Chain the pipeline to sort the resulting subordinates by `name` (ascending), then apply the appropriate pagination logic using `$skip` and `$limit` based on the `page` (1-indexed) and `limit` query parameters.
3. Use the MongoDB shell (`mongosh`) to connect to the `corp` database and create an ascending index on `managerId` in the `employees` collection to optimize the execution plan.
4. Start the API server so it listens on `127.0.0.1:8000`. Leave it running in the background.

To verify success, ensure that:
- The API is running on `127.0.0.1:8000`.
- Calling `curl "http://127.0.0.1:8000/api/subordinates?manager_id=1&page=2&limit=2"` returns a valid JSON array of exactly 2 employee objects (assuming enough data exists), correctly sorted by name.
- The MongoDB index on `managerId` exists.