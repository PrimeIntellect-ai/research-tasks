You are a platform engineer responsible for maintaining our custom CI/CD pipeline orchestrator. We have a legacy system that defines microservices, their versions, and their build dependencies in a JSON configuration file. 

Recently, a developer submitted a patch (`/home/user/ci_update.patch`) to update the versions in our base configuration (`/home/user/ci_config.json`). 

Your task involves several steps to update the configuration, resolve the build graph, and generate the necessary build artifacts.

**Step 1: Apply the Patch**
Apply the unified diff patch `/home/user/ci_update.patch` to `/home/user/ci_config.json`. Ensure the patch is applied cleanly.

**Step 2: Write the Build Orchestrator**
Create a Python script at `/home/user/builder.py` that does the following:
1. Reads the updated `/home/user/ci_config.json`. The JSON contains a `services` dictionary. Each service has a `version` (Semantic Versioning: MAJOR.MINOR.PATCH) and a `depends_on` list. Each dependency specifies the `name` of the required service and a `requires` string (which will always be in the format `>=X.Y.Z`).
2. Implements a custom directed acyclic graph (DAG) data structure to represent the services and their dependencies.
3. Implements semantic version comparison to verify if the dependencies are satisfied. For a service to be built, **all** its dependencies must be present in the config, and the configured version of the dependency must satisfy the `>=X.Y.Z` requirement. If a service's dependencies are NOT met, it (and any service depending on it) must be excluded from the build plan.
4. Performs a topological sort of the DAG to determine the build order of the valid services. *Important tie-breaking rule:* If multiple services can be built at the same time (i.e., they have no pending dependencies), they must be ordered alphabetically by their service name.
5. Writes the final valid build sequence to `/home/user/build_order.log`, with one service name per line.
6. Generates a valid `/home/user/Makefile`. The Makefile must contain a target for each valid service. The target name must be the service name. The command for each target should simply be `@echo "Building <service_name> v<version>"`. Also, add an `all` target at the top that depends on all valid services in the correct topologically sorted order.

**Execution:**
Once you have written the script, run it.
Do not use any external pip packages like `semver` or `networkx`. You must implement the semantic version parsing and DAG topological sort using Python standard libraries only.

**Verification:**
The automated tests will verify:
1. The `ci_config.json` is correctly patched.
2. The `/home/user/build_order.log` contains the exact correct alphabetical-topological order of valid services.
3. The `/home/user/Makefile` is structurally correct and matches the resolved DAG.