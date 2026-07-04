You are assisting a compliance officer in auditing system access logs. We have an internal Rust-based access control evaluation engine, `rbac_engine`, which analyzes schema relationships and computes shortest paths in our permission graph to determine if a user has access to a resource.

Recently, the source code for this engine was vendored into our environment at `/app/rbac_engine-0.1.0`, but it is currently failing to build due to a deliberate perturbation introduced during the vendoring process (specifically, issues in its `Makefile` and environment configuration). 

Your task is to:
1. Fix the build configuration for `/app/rbac_engine-0.1.0` so that running `make build` successfully compiles the Rust binary `rbac-cli`.
2. Understand how `rbac-cli` works by analyzing its source code. It takes a schema file and an access request.
3. Create a bash script at `/home/user/audit.sh` that acts as a classifier for access requests. 
   - The script must take exactly one argument: the absolute path to a JSON file containing a single access request.
   - The script must evaluate the request against the schema located at `/app/schema/system_graph.yaml` using the compiled `rbac-cli`.
   - The script must print exactly `ALLOW` to standard output if the access is valid according to the schema, and `DENY` if it is invalid. It should return exit code 0 in both cases.

Your solution will be tested against two corpora of access requests:
- A "clean" corpus of legitimate access requests that must all evaluate to `ALLOW`.
- An "evil" corpus of compliance-violating access requests (unauthorized traversals) that must all evaluate to `DENY`.

Ensure your script is executable and relies only on standard bash tools and the compiled `rbac-cli` binary.