As a compliance officer, I need to audit our financial transaction systems for potential money laundering networks. Our raw transactional data and entity records are stored in a PostgreSQL database, but detecting complex circular flows and key intermediary accounts requires graph analytics.

We have a multi-service environment running locally:
1. **PostgreSQL** (Port 5432): Contains the raw tables `entities` (id, name, is_sanctioned) and `transactions` (sender_id, receiver_id, amount, timestamp).
2. **Neo4j** (Port 7687 for Bolt, 7474 for HTTP): An empty graph database ready for analysis.
3. **Rust Audit Service**: A boilerplate Rust project located in `/home/user/audit_service/`.

Your task is to complete the Rust service to perform the following compliance audit workflow:
1. **Graph Materialization**: Extract the entities and transactions from PostgreSQL and project them into the Neo4j database. Entities should be `Account` nodes, and transactions should be `TRANSFERRED_TO` directed edges with `amount` as a property.
2. **Graph Analytics**: Calculate the Betweenness Centrality for all `Account` nodes in Neo4j to identify potential money laundering hubs (intermediaries). Assign this score to a property `risk_score` on each node.
3. **Graph Traversal**: Find all shortest paths between any node where `is_sanctioned = true` and any node with a `risk_score` in the top 5% of all nodes. 
4. **Output**: The Rust service must output a JSON file at `/home/user/compliance_report.json` containing an array of objects. Each object should represent a discovered path, containing the `sanctioned_id`, `hub_id`, and `path_length`.

The automated verifier will evaluate your solution based on the correctness of the generated paths and the execution time of the entire workflow. Your Rust application must complete the end-to-end process in under 15 seconds for a dataset of 50,000 transactions.

Please write the necessary Rust code using `tokio`, `sqlx` (for Postgres), and `neo4rs` (for Neo4j), build the project in release mode, and run it to produce the `compliance_report.json`.