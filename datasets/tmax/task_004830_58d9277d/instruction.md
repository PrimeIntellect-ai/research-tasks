You are a Database Reliability Engineer (DBRE) managing a complex microservices architecture. Your company's infrastructure data is stored across three different datastores (relational, document, and graph) and backed up nightly. You need to write a Python script to cross-reference and aggregate these backups to ensure data consistency across the representations.

You have three backup files in `/home/user/backups/`:
1. `services.csv` (Relational backup export): Contains `service_id`, `service_name`, and `team_owner`.
2. `endpoints.jsonl` (Document backup export): Contains one JSON object per line with `service_id` and a list of `endpoints` exposed by that service.
3. `dependencies.json` (Graph backup export): A JSON array of edges representing service dependencies, where each object has a `source` (service_id) and `target` (service_id).

Write a Python script at `/home/user/verify_backups.py` that processes these three files and generates a team-level summary of the infrastructure. The script must create a file at `/home/user/team_summary.json` containing a single JSON object where:
- The keys are the `team_owner` names.
- The values are objects containing:
  - `total_endpoints`: The total number of unique endpoints managed by services owned by this team.
  - `outbound_dependencies`: The total number of outbound dependencies (edges where the `source` is a service owned by this team).

Example output format for `/home/user/team_summary.json`:
```json
{
  "TeamAlpha": {
    "total_endpoints": 3,
    "outbound_dependencies": 1
  },
  "TeamBeta": {
    "total_endpoints": 3,
    "outbound_dependencies": 2
  }
}
```

Ensure your script runs successfully and produces the exact required output format.