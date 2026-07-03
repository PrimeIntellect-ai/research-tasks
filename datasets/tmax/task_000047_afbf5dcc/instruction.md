You are a platform engineer maintaining a CI/CD pipeline. We are modernizing our deployment gatekeeper, replacing a legacy validation step with a robust, pure-Python solution.

Currently, incoming microservice deployment manifests are validated by a mix of ad-hoc scripts and a legacy, stripped C binary located at `/app/legacy_route_validator`. This binary checks URL route definitions for security violations, but it is slow and unmaintained.

Your task is to write a single Python script at `/home/user/ci_filter.py` that acts as the new CI gatekeeper. Your script must accept a single command-line argument: the path to a directory containing deployment manifest JSON files. It should evaluate each JSON file in the directory and print the absolute path of the files that are strictly **VALID**, one per line. Invalid files should be silently ignored.

A manifest JSON file has the following structure:
```json
{
  "service_name": "auth_service",
  "dependencies": {"auth": ["db", "cache"], "cache": [], "db": []},
  "schema_migration": "CREATE TABLE users (id INT);",
  "routes": ["/api/v1/login?user=test", "/api/v1/logout"]
}
```

To be **VALID**, a manifest must pass ALL the following checks:
1. **Dependency Graph Resolution:** The `dependencies` dictionary represents a directed graph where keys depend on the list of values. The graph MUST be a valid Directed Acyclic Graph (DAG) capable of being topologically sorted. If there is a cycle, the manifest is invalid.
2. **Schema Migration Safety:** The `schema_migration` string MUST NOT contain the substring `DROP TABLE` (case-insensitive).
3. **URL Routing and Parameter Validation:** Every URL in the `routes` list must be considered safe according to the rules encoded in the legacy binary `/app/legacy_route_validator`. You must reverse-engineer this stripped binary (using tools like `strings`, `objdump`, `ltrace`, or simply by black-box testing it) to understand its exact filtering rules, and reimplement those rules in your Python script. Do NOT call the binary from your script; reimplement its logic. (Hint: The binary takes a single URL string as an argument and exits with code 0 if safe, or code 1 if malicious).

You can use the standard library for Python. Make sure your script is executable (`chmod +x /home/user/ci_filter.py`).