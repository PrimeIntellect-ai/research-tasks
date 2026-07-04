You are acting as a release manager for a suite of web microservices. The configuration for these microservices is defined in a set of JSON files located in the `/home/user/release/services` directory. Each file represents a specific version of a microservice, detailing its dependencies (using semantic versioning), its URL routing endpoints, and the allowed HTTP methods and parameters for web security.

Currently, there is a build failure because some developers introduced a circular dependency in the newer versions of the services. 

Your task is to write a bash script at `/home/user/release/build_release.sh` that performs the following actions:

1. **Dependency Resolution (Constraint Satisfaction & Semantic Versioning):**
   Read all JSON files in `/home/user/release/services`. Each JSON file contains `name`, `version`, and a `requires` object specifying dependencies (e.g., `">= 1.0.0"`). 
   Your script must select exactly one version for each available service such that all `requires` constraints are satisfied *and* no circular dependencies are formed in the selected set. 
   The script must output the resolved list of services and their selected versions to `/home/user/release/lockfile.txt` in the format `service_name=version`, one per line, sorted alphabetically by service name.

2. **WAF Router Generation (Serialization, Code Translation, & Routing):**
   Once the valid, non-circular set of service versions is determined, extract the `routes` array for those specific versions. 
   Translate these JSON routing rules into a standalone Bash executable named `/home/user/release/waf_router.sh`. 
   
   The generated `/home/user/release/waf_router.sh` must:
   - Accept exactly three arguments: `METHOD`, `PATH`, and `QUERY_STRING` (e.g., `./waf_router.sh GET /api/users id=5&sort=asc`).
   - Route the request by printing `ROUTED_TO: <service_name>` if the METHOD and PATH strictly match a route defined in the selected services, AND all provided parameters in the `QUERY_STRING` are present in the route's `allowed_params` list. (Query parameters are separated by `&` and formatted as `key=value`. Check only the keys).
   - If the method or path does not match, or if an unallowed parameter is present, print exactly `403 FORBIDDEN`.
   - If a path matches but no query string is provided, and the route has allowed parameters, it is still valid (allowed parameters are optional, but no *extra* parameters are permitted). If `QUERY_STRING` is empty or omitted, handle it gracefully.

**Execution:**
Your solution must be written entirely in Bash (standard CLI tools like `jq`, `grep`, `awk`, `sed`, `sort` are allowed). Do not use Python, Node.js, or other scripting languages. Ensure your `build_release.sh` has executable permissions.