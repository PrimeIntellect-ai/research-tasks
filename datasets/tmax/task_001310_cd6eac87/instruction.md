You are helping a researcher organize a graph dataset of academic researchers and institutions. 

We have a SQLite database at `/app/dataset.db` containing a knowledge graph with two tables:
1. `nodes` (`id` TEXT PRIMARY KEY, `label` TEXT, `region` TEXT)
   - Labels are either `'researcher'` or `'institution'`.
2. `edges` (`source` TEXT, `target` TEXT, `type` TEXT)
   - `type` is always `'affiliated_with'`.
   - `source` is a researcher ID, `target` is an institution ID.

Unfortunately, the script that generated the `edges` table had a bug (an implicit cross join), resulting in millions of false `'affiliated_with'` edges. 

The researcher left a scanned note in `/app/schema_rule.png` that explains the business logic for which edges are actually valid based on the data model. You will need to extract the rule from this image (e.g., using `tesseract`) to reverse engineer the correct data model relationships.

Your task is to:
1. Read the rule from `/app/schema_rule.png` to understand how to filter the valid edges.
2. Write and run a Rust-based HTTP web service that calculates the correct graph degree centrality based on the cleaned edges.
3. The Rust web service MUST listen on `127.0.0.1:8080`.
4. It must expose exactly one endpoint:
   - `GET /top-affiliations`
   - It should return a JSON array of the top 3 `'researcher'` IDs with the highest number of valid `'affiliated_with'` edges.
   - The JSON should look like: `[["researcher_123", 5], ["researcher_456", 4], ["researcher_789", 4]]`.
   - Sort the results by the count of valid affiliations in descending order. If there is a tie, sort by the researcher's `id` in ascending order.

You may use any Rust web framework (e.g., `axum`, `actix-web`, `hyper`) and SQLite client (e.g., `rusqlite`). Create a new Cargo project in `/home/user/graph_api` to build your service. Once the service is running, leave it running in the background so it can be tested.