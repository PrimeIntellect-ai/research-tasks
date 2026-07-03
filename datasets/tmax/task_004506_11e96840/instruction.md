We are in the process of migrating a legacy Python 2 microservice to a modern Python 3 microservice. To ensure a safe rollout, we are building a Go-based "shadow proxy" that mirrors traffic to both services, transforms the legacy payload to match the new schema, and generates a diff of the responses.

You have been provided a workspace in `/home/user/migration_test`.
In this directory, you will find:
- `legacy_service.py` (simulating the Python 2 service, listening on port 8022)
- `new_service.py` (simulating the Python 3 service, listening on port 8033)
- `proxy.go` (The Go shadow proxy, listening on port 8080)
- `run_requests.sh` (A script that sends traffic to the proxy)

Your tasks are as follows:

1. **Memory Debugging**: The current `proxy.go` has a severe memory leak located in how it tracks request history. Use Go's `net/http/pprof` to identify the leak, then modify `proxy.go` to fix it (remove the global slice append that causes the leak). After fixing it, start the server and save a heap profile to `/home/user/migration_test/mem.prof` using curl against the pprof endpoint.

2. **URL Routing and Parameter Parsing**: Update `proxy.go` to correctly parse incoming GET parameters and append them exactly as received to the backend requests made to ports 8022 and 8033. For example, `/api/user?id=123&verbose=true` should be requested as `/api/user?id=123&verbose=true` on both backends.

3. **Schema Migration & Diff Processing**: 
   - The legacy Python 2 service returns JSON with `snake_case` keys. The new Python 3 service uses `camelCase` keys.
   - Before comparing, your Go proxy must parse the legacy Python 2 JSON response and recursively convert all dictionary keys from `snake_case` to `camelCase` (e.g., `user_name` becomes `userName`, `created_at` becomes `createdAt`).
   - Compare the transformed legacy JSON with the new service JSON (both formatted with 2-space indentation).
   - If they differ, generate a unified diff. Append the unified diff to `/home/user/migration_test/diff_results.log`. If they perfectly match, write nothing to the log for that request.

Run the mock services in the background:
`python3 legacy_service.py &`
`python3 new_service.py &`

Run your fixed Go proxy, then execute `bash run_requests.sh`. Ensure the diff log and the memory profile are generated exactly at the specified paths.