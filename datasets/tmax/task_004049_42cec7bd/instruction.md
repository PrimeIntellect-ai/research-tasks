You are assisting a compliance officer auditing an internal network for a security review. We need to determine the shortest SSH access path from the public-facing web server to a secure vault.

You have been provided with a Rust project located at `/home/user/audit`. Inside this directory, there is:
1. A JSON file `/home/user/audit/systems.json` containing a mapping of systems. It is an array of objects, each with an `id` (integer) and `name` (string).
2. A SQLite database `/home/user/audit/access.db` containing a table `network_links (source_id INTEGER, target_id INTEGER, protocol TEXT)`.

Your task is to write the Rust program in `/home/user/audit/src/main.rs` to perform the following:
1. Parse `systems.json` to map system names to their respective integer IDs.
2. Connect to the `access.db` SQLite database.
3. Use a parameterized SQL query to extract all network links where the protocol is exactly "SSH".
4. Build a directed graph representing these SSH connections.
5. Compute the shortest path (minimum number of hops) from the system named "PublicWeb" to the system named "SecureVault".
6. Write the integer value of the shortest path length to the file `/home/user/audit/shortest_path.txt`. If no path exists, write `-1`.

The Rust project has already been initialized, and `Cargo.toml` includes dependencies for `rusqlite` and `serde_json`. You just need to write the code in `src/main.rs`, run the project with `cargo run`, and ensure the output file is generated correctly.