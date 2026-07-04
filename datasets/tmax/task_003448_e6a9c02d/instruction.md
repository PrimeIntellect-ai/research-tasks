You are a Database Reliability Engineer (DBRE) tasked with ensuring the integrity of our backup systems. Our backup artifacts form a complex dependency graph (full backups, incrementals, and differentials) tracked across multiple services. 

We have an environment composed of two cooperating services:
1. **PostgreSQL (port 5432)**: Stores the graph metadata of backup chains.
   - Database: `backups_db`
   - User: `backup_admin`, Password: `secretpassword`
   - Table `backup_nodes`: `id` (VARCHAR), `parent_id` (VARCHAR, nullable), `backup_type` (VARCHAR: 'FULL', 'INCREMENTAL', 'DIFFERENTIAL'), `size_bytes` (BIGINT).
2. **Redis (port 6379)**: Stores the NoSQL document manifests for rapid retrieval and schema validation.
   - Keys are formatted as `manifest:<backup_id>`.
   - Values are JSON strings containing `{"checksum": "<sha256>", "status": "AVAILABLE" | "ARCHIVED"}`.

A startup script located at `/app/start_services.sh` brings up these services and populates them. Your first step should be to run this script.

Your task is to create a Rust-based CLI tool that acts as a backup manifest validator. You must create a new Cargo project at `/home/user/backup_validator`. 

The tool must take a single file path as an argument. The file will contain a JSON manifest.
Example invocation: `cargo run -- /path/to/manifest.json`

The CLI must parse the JSON manifest (which contains a single `backup_id` field) and perform the following verifications:
1. **Graph Traversal (SQL Recursive CTE)**: Query PostgreSQL to traverse the dependency graph from the given `backup_id` up to its root. 
   - A valid chain MUST eventually reach a node with `backup_type = 'FULL'`.
   - The chain MUST NOT contain any cycles (e.g., an incremental backing up to itself or a descendant).
   - If the root is not 'FULL' or a cycle is detected, the manifest is invalid.
2. **NoSQL Validation**: Query Redis for the key `manifest:<backup_id>`. 
   - The JSON value must have `status` strictly equal to `"AVAILABLE"`.
3. **Output Schema**: Ensure the manifest's structural integrity.

**Acceptance Criteria:**
If the manifest is perfectly valid according to the rules above, the CLI must terminate with **Exit Code 0** and print `ACCEPT`.
If the manifest violates ANY of the rules (missing parent, cycle detected, missing in Redis, status not AVAILABLE, invalid JSON), the CLI must terminate with **Exit Code 1** and print `REJECT`.

**Adversarial Corpus Verification:**
We have provided two corpora of test manifests:
- `/app/corpus/clean/`: Contains manifests that are completely valid. Your tool must ACCEPT 100% of these.
- `/app/corpus/evil/`: Contains malicious, cyclic, or corrupted manifests. Your tool must REJECT 100% of these.

You must build the tool and verify it passes both corpora perfectly. Leave the final compiled binary at `/home/user/backup_validator/target/release/backup_validator`.