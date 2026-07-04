You are helping us migrate a legacy Python 2 data processing pipeline to a modern Go-based architecture. The pipeline processes a dependency graph of transformation nodes, each containing a tiny custom bytecode payload that represents operations. 

We use a multi-service setup. A startup script at `/app/startup.sh` brings up a Redis instance on `127.0.0.1:6379`. Redis is populated with the legacy data.

Your task is divided into three stages:

**Stage 1: Fix the Legacy Extraction Tool**
There is a legacy tool at `/app/py_graph_dumper`. We attempted to migrate it to Python 3, but the `setup.py` is broken, and there are lingering Python 2 syntax issues in `dumper.py`.
1. Fix the `setup.py` and `dumper.py` so the package can be installed via `pip install -e /app/py_graph_dumper`.
2. Run the installed tool: `dumper --output /tmp/legacy_schema.json`. This tool connects to Redis, reads the `legacy:nodes` hash, and dumps the raw JSON schema.

**Stage 2: Implement the Go Processor**
In `/app/go-processor`, we have scaffolded a Go project. You need to implement the core logic in `processor.go` and `server.go`.
1. **Graph Traversal & Sorting:** Parse `/tmp/legacy_schema.json`. Perform a topological sort on the nodes based on their `deps` (dependencies) arrays. If node A depends on node B, B must appear before A in the sorted output.
2. **Assembly / Bytecode Analysis:** Each node in the JSON has a `bytecode` field containing a hex string (e.g., `"0103"`). You must write a function to translate this hex string into our minimal assembly format. The mapping is:
   - `00` -> `NOP`
   - `01` -> `PUSH`
   - `02` -> `POP`
   - `03` -> `ADD`
   Join the translated instructions with a space (e.g., `"0103"` -> `"PUSH ADD"`).
3. **Schema Migration:** Create a function `MigrateSchema()` that takes the topologically sorted nodes, applies the bytecode translation to a new field called `asm`, and saves the ordered list of node IDs as a JSON array to the Redis key `v2:ordered_nodes`. Also, save a Redis Hash at `v2:nodes` where the keys are node IDs and values are the new JSON representation of the nodes (including the `asm` string).

**Stage 3: Expose Multi-Protocol Endpoints**
The Go application must start and listen on two ports:
1. **HTTP Server on `127.0.0.1:8080`:** 
   - `POST /migrate` - Triggers the `MigrateSchema()` function. Returns HTTP 200 OK on success.
   - `GET /node/{id}` - Returns the JSON of a migrated node from Redis `v2:nodes`.
2. **TCP Server on `127.0.0.1:9000`:**
   - Accepts simple text commands. If a client sends a node ID followed by a newline (e.g., `node_A\n`), the server must respond with the translated `asm` string followed by a newline (e.g., `PUSH ADD\n`).

Once implemented, compile and run your Go service in the background. Leave it running so our automated verifier can test the HTTP and TCP endpoints and inspect the Redis database. Create a file `/tmp/success.log` containing the word `READY` when your services are up and running.