You are an operations engineer tasked with automating the fix for a Rust project that currently fails to compile due to outdated dependency versions and a stale data schema. The project is located at `/home/user/project`. 

You must use **Python** to write the automation scripts that resolve these issues. 

Please perform the following steps:

1. **Semantic Version Resolution:** 
   The project's dependencies in `/home/user/project/Cargo.toml` violate the minimum version policies. 
   Read `/home/user/project/policy.json`, which contains a mapping of dependencies to their minimum allowed semantic versions (e.g., `>=1.0.130`). 
   Write and execute a Python script at `/home/user/project/fix_deps.py` that reads `Cargo.toml` and `policy.json`, then updates the dependency versions in `Cargo.toml` to exactly the minimum versions specified in the policy (i.e., extract the version string after `>=` and replace the old version in `Cargo.toml`).

2. **Structured Data Schema Migration:** 
   The Rust code expects a data file in a new format, but the system only has the legacy `/home/user/project/schema_v1.json`. 
   Write and execute a Python script at `/home/user/project/migrate.py` that reads `schema_v1.json`. The legacy format is a list of objects containing `id`, `first_name`, and `last_name`. Your script must transform this into a new file at `/home/user/project/data.json` containing a list of objects with only `id` and `full_name` (where `full_name` is the concatenation of `first_name` and `last_name` separated by a single space).

3. **CI/CD Pipeline Setup:** 
   To prevent future regressions, create a continuous integration bash script at `/home/user/project/ci_pipeline.sh`. This script must:
   - Start with `#!/bin/bash`
   - Navigate to `/home/user/project`
   - Run `cargo check`
   - Exit with the exact exit code of the `cargo check` command.
   Ensure the script is made executable (`chmod +x`).

Complete these tasks so that automated verification can check the updated `Cargo.toml`, the generated `data.json`, and the executable `ci_pipeline.sh`.