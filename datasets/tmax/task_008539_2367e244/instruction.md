You are an engineer tasked with porting a CI/CD artifact verification and dependency resolution tool to run inside a minimal, highly restricted Linux container. The container lacks advanced scripting languages (like Python) or build tools (like Make), so you must implement the logic entirely in pure Bash using standard Coreutils.

Your task is to create a Bash script at `/home/user/resolve_build.sh` that reads a custom dependency graph file, verifies the integrity of the build artifacts, and determines the correct execution order for the CI/CD pipeline.

**System State & Inputs:**
1. **Artifacts Directory:** `/home/user/artifacts/` contains several file artifacts.
2. **Graph File:** `/home/user/ci_deps.graph` contains the custom data structure defining the build graph. 

The `ci_deps.graph` file has the following custom format (one artifact per line):
`ARTIFACT_NAME : SHA256_CHECKSUM : DEPENDENCY_1,DEPENDENCY_2,...`
*   `ARTIFACT_NAME`: The name of the file in the artifacts directory.
*   `SHA256_CHECKSUM`: The expected SHA-256 hash of the artifact.
*   The third field is a comma-separated list of artifacts that must be built *before* this artifact. If there are no dependencies, this field will be empty or contain just whitespace.

**Requirements for `/home/user/resolve_build.sh`:**
1. **Checksum Verification:** The script must read `ci_deps.graph` and verify the SHA-256 checksum of every artifact listed against the actual files in `/home/user/artifacts/`.
    *   If any artifact fails the checksum verification or is missing, the script must output `ERROR: <ARTIFACT_NAME>` to `stdout` and immediately exit with status code `1`.
2. **Graph Traversal & Resolution:** If all checksums pass, the script must perform a topological sort on the dependencies to determine the valid build order.
    *   Assume the graph is a valid Directed Acyclic Graph (DAG) with no circular dependencies.
    *   *Tie-breaking rule:* Whenever there are multiple artifacts available to be built (i.e., their dependencies are met), you must process them in **alphabetical order**.
3. **Output:** The script must write the final resolved build order to `/home/user/build_plan.txt`, with one `ARTIFACT_NAME` per line, and exit with status code `0`.

**Constraints:**
* The script must be written in Bash and use only standard shell built-ins and coreutils (e.g., `sha256sum`, `awk`, `sed`, `grep`). No `python`, `perl`, `make`, `jq`, or `tsort` (you must implement the topological sort logic yourself).
* Make sure `/home/user/resolve_build.sh` is executable (`chmod +x`).

Implement the script and run it to produce `/home/user/build_plan.txt`.