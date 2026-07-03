You are the release manager for our embedded telemetry platform. We are deploying a new Rust-based telemetry ingestion service, but we have a few critical issues blocking the release.

Your task consists of three phases:

**Phase 1: Reverse-engineer the legacy checksum algorithm**
Our edge devices send data payloads protected by a custom 32-bit checksum. The original source code for the checksum algorithm was lost. We only have a stripped, compiled binary `/app/legacy_chksum` that implements it. 
You must analyze or black-box test `/app/legacy_chksum` to figure out the algorithm. It takes a single file path as an argument and prints the 32-bit checksum in hex format. You need to reimplement this exact logic in our new Rust server to validate incoming packets.

**Phase 2: Fix the memory leak in the Rust Ingestion Server**
There is a drafted Rust TCP server at `/home/user/ingester`. It successfully binds to port `9999` and reads payloads, but our profiling showed it has a catastrophic memory leak on every request due to mishandled buffer allocations in the packet reading loop. 
Fix the memory leak in `/home/user/ingester/src/main.rs`. Ensure the server is robust and drops invalid packets (where the checksum does not match the payload).

**Phase 3: Schema Migration and Integration**
The Rust service writes to an SQLite database at `/home/user/telemetry.db`.
1. Before starting the server, you must migrate the database. The existing table `readings_v1` (columns: `id INTEGER`, `dev_id INTEGER`, `metric REAL`) must be migrated to a new table `readings_v2` (columns: `id INTEGER PRIMARY KEY`, `device_id INTEGER`, `temperature REAL`). All existing data must be migrated over (map `dev_id` -> `device_id` and `metric` -> `temperature`).
2. Modify the Rust server so that it inserts valid incoming payloads into `readings_v2`.

**Protocol Specification:**
The server must listen on TCP `127.0.0.1:9999`.
The protocol is a simple binary stream per connection:
- 4 bytes: Payload length `N` (unsigned 32-bit integer, little-endian)
- 4 bytes: Checksum (unsigned 32-bit integer, little-endian)
- `N` bytes: The payload itself, which is a JSON string of the format `{"device": <int>, "temp": <float>}`

If a packet is valid (checksum matches the payload according to the legacy algorithm), insert it into `readings_v2`. If invalid, immediately drop the TCP connection.

Compile your fixed server and leave it running in the background listening on `127.0.0.1:9999` so our integration tests can verify it.