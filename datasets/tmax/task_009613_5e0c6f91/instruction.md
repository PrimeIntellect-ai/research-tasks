You are helping a team migrate a massive legacy mathematical data-processing pipeline from Python 2 to Python 3. As part of this, you need to write a Go tool that analyzes the old Python 2 scripts, resolves their dependency graph, calculates execution weights, computes checksums to ensure code integrity, and plans the database schema migrations.

The legacy Python 2 scripts are located in `/home/user/legacy_pipeline/`.
Each script contains a header with metadata in the following format:
```python
# DEPENDS_ON: scriptA.py, scriptB.py
# SCHEMA_VERSION: v1.2
# WEIGHT_FACTOR: 5
```
(Note: `DEPENDS_ON` might be empty or missing if there are no dependencies. Comma-separated if multiple).

Your task is to write a Go program in `/home/user/migrator/main.go` that does the following:

1. **Graph Traversal & Dependency Resolution:** 
   Parse all `.py` files in `/home/user/legacy_pipeline/`. Build a dependency graph and determine the correct execution order (topological sort). If multiple scripts can be executed at the same level (i.e., they have the same depth/dependencies resolved), sort them alphabetically by filename to ensure deterministic ordering.

2. **Numerical Algorithm (Weight Calculation):**
   Calculate the `total_weight` for each script. 
   `total_weight` = The script's own `WEIGHT_FACTOR` + the sum of the `total_weight` of all its direct dependencies.

3. **Checksum Calculation:**
   Compute a SHA-256 checksum (in hex format) for each script's source code *excluding* the metadata header. Specifically, ignore any line that begins with `#`. Join the remaining lines with newline characters (`\n`) and compute the SHA-256 hash.

4. **Schema Migration Logic:**
   The `SCHEMA_VERSION` follows a `v[MAJOR].[MINOR]` format. Your tool must plan the target schema for the Python 3 rewrite by incrementing the major version by 1 and setting the minor version to 0 (e.g., `v1.2` becomes `v2.0`, `v2.9` becomes `v3.0`).

5. **Cross-Compilation:**
   The tool needs to be distributed to different teams. Build the Go program for both Linux and Windows (amd64 architecture). 
   Save the binaries as:
   - `/home/user/migrator/build/migrator-linux`
   - `/home/user/migrator/build/migrator-windows.exe`

6. **Execution and Output:**
   Run your Linux binary to generate a JSON report at `/home/user/migration_plan.json`.
   The JSON must be a list of objects, ordered strictly by the resolved topological execution order, with the following format:
   ```json
   [
     {
       "script": "base.py",
       "total_weight": 10,
       "checksum": "a1b2c3d4...",
       "target_schema": "v2.0"
     }
   ]
   ```

Write the Go code, build the binaries, and generate the final `migration_plan.json`.