Can you help me review and fix a broken PR for our open-source API gateway project? 

The PR attempts to add a custom expression parser for advanced GraphQL filtering, but the maintainers suspect it introduced a severe Web Security vulnerability (specifically, memory exhaustion and unauthorized schema access via nested expressions). We have a multi-service setup locally.

Here is the environment under `/home/user/app/`:
- **Nginx** (Reverse Proxy) listening on port 8080.
- **Python FastAPI** (GraphQL Endpoint) listening on port 8000.
- **Redis** (Caching layer) listening on port 6379.

Your task is to implement a robust Python-based sanitizer/detector script at `/home/user/app/sanitizer.py`. 
It must expose a function `def is_safe_query(query_string: str) -> bool:`.
You need to analyze the GraphQL queries, parse the custom expressions, and detect malicious patterns (like deep nesting causing memory blowouts or unauthorized field access).

When we run our test suite, we will pass a batch of queries to your script. 
1. `is_safe_query` must return `True` for valid, safe filtering expressions.
2. `is_safe_query` must return `False` for malicious queries designed to exploit the memory parser or access restricted migrated schema fields.

Please investigate the services, understand the expression evaluation logic currently in the PR (located in `/home/user/app/api/parser.py`), and write the `sanitizer.py` script. Finally, ensure Nginx, FastAPI, and Redis are properly glued together—update `/home/user/app/nginx.conf` to route `/graphql` traffic to the FastAPI backend, and restart the services using the provided `/home/user/app/start_services.sh` script.