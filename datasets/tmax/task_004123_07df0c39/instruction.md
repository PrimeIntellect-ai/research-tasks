As a compliance officer, I need to audit our multi-database architecture to verify data access lineages. Our system uses multiple cooperating data services:
1. PostgreSQL (running on port 5432): Contains the Identity and Access Management (IAM) relational data. The `users` table maps `user_id` to `role_id`. The `roles` table defines role hierarchies (`role_id`, `parent_role_id`).
2. MongoDB (running on port 27017): Contains our unstructured `audit_logs` database with an `events` collection. Each document records an access event, structured as `{ "actor_role_id": <int>, "accessed_resource_id": <int>, "timestamp": <str> }`.

Currently, these services are configured but not glued together for our compliance tool. There is a startup script at `/app/start_services.sh` which launches these databases.

Your task is to:
1. Reconfigure and connect to these services using the credentials provided in `/home/user/db_config.env` (you will need to source or parse this file).
2. Write a Rust CLI application in `/home/user/compliance_auditor` (initialize it with Cargo).
3. The Rust application must take exactly two arguments: `--user <int>` and `--resource <int>`.
4. The application must safely parameterize queries to read the relational user-role data from PostgreSQL and the document-based event data from MongoDB.
5. Combine these representations into an in-memory graph to compute the shortest access path from the specified user to the target resource. A path exists if a user holds a role (or inherits it via `parent_role_id`) that has an access event for the resource, OR if there is a chain of resources accessed by roles the user can assume.
6. The program must output a strictly validated JSON schema to stdout: `{"path_exists": true/false, "shortest_path_length": <int or null>, "roles_involved": [<int>]}`.

A compiled reference implementation (oracle) that performs this exact graph traversal and schema validation is located at `/app/oracle_auditor`. Your Rust program's output must perfectly match the oracle's output for any combination of user and resource IDs. Ensure your code is optimized for rapid querying so it can handle automated fuzz testing.