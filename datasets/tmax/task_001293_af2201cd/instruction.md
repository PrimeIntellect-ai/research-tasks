You are acting as a systems engineer for a compliance auditing team. The compliance officers need a unified API to audit database logs and automatically detect transaction deadlocks to enforce compliance standards.

Currently, the infrastructure team has provided two internal microservices located in `/app/`:
1. **Log Service**: A service running on `127.0.0.1:8001` that provides raw transaction wait-for logs. You can start it via `/app/log_service/start.sh`. It exposes `GET /logs` which returns a JSON array of objects: `[{"tx": "T1", "waiting_for": "T2"}, ...]`. 
2. **Auth Service**: A service running on `127.0.0.1:8002` that validates compliance officer API tokens. You can start it via `/app/auth_service/start.sh`. It exposes `POST /validate` which accepts `{"token": "<token_string>"}` in the JSON body and returns HTTP 200 if valid, or HTTP 403 if invalid.

Your task is to write and start a new API service (using any language or bash tools of your choice) listening on `127.0.0.1:9000`. This service must act as the unified compliance gateway.

Requirements for your service:
1. **Endpoint**: It must expose `GET /api/audit/deadlocks`.
2. **Authentication**: It must require an `Authorization: Bearer <token>` header. It must forward the token to the Auth Service for validation. If the Auth Service returns 403, your service must return HTTP 401 Unauthorized.
3. **Graph Projection & Deadlock Detection**: If authorized, it must fetch the raw logs from the Log Service. It must build a "wait-for" graph from the logs and detect all deadlocks. A deadlock is defined as any simple cycle in the wait-for graph (e.g., T1 waits for T2, T2 waits for T1).
4. **Sorting & Filtering**: 
   - Extract the transaction IDs involved in each isolated cycle.
   - For each cycle, sort the transaction IDs alphabetically to create a canonical representation (e.g., `["T1", "T2", "T3"]`).
   - Remove duplicate cycles (since a cycle might be found starting from different nodes).
   - Sort the overall list of cycles alphabetically by their first element, then second, etc.
5. **Pagination**: The endpoint must accept `page` (1-indexed) and `limit` query parameters. It must return a paginated slice of the sorted cycles.
6. **Response Format**: It must return a JSON response exactly like this (HTTP 200):
   ```json
   {
     "total_deadlocks": 5,
     "page": 1,
     "limit": 2,
     "data": [
       ["T1", "T2", "T3"],
       ["T4", "T5"]
     ]
   }
   ```

To complete the task:
- Ensure all three services (Log, Auth, and your Gateway) are running in the background.
- You do not need to persist data; fetching from the Log Service on every request is acceptable.
- Keep your Gateway running so the automated verification system can send HTTP requests to it.