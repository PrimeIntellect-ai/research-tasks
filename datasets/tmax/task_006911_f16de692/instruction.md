You are a QA engineer responsible for setting up isolated test environments. To bring up the environment, multiple microservices must be started in the correct dependency order, and each must be assigned a unique port from its allowed range to avoid conflicts.

Your task is to write a pure Bash script at `/home/user/resolve_env.sh` that performs dependency resolution (graph traversal) and port allocation (constraint satisfaction).

The script must accept two file arguments:
1. `deps_file`: A text file defining service dependencies.
2. `ports_file`: A text file defining allowed port ranges.

**Input Formats:**
- The `deps_file` contains lines in the format: `Service: Dep1 Dep2 ...`
  This means `Service` depends on `Dep1` and `Dep2`, so `Dep1` and `Dep2` must start *before* `Service`. Services with no dependencies are written as `Service:` (with a trailing colon but no dependencies).
- The `ports_file` contains lines in the format: `Service: MIN_PORT-MAX_PORT`

**Requirements:**
1. **Topological Sort:** The script must determine the startup order of the services. 
   - A service can only be started once all its dependencies have been started.
   - **Tie-breaking rule:** If multiple services are eligible to start at the same time, always pick the one that comes first alphabetically.
   - Write the resolved startup order to `/home/user/startup_order.txt`, one service name per line.

2. **Port Allocation:** Once the startup order is determined, assign exactly one port to each service.
   - Process the services in the exact startup order determined above.
   - For each service, assign the *lowest possible port* within its allowed range (inclusive) that has *not already been assigned* to an earlier service.
   - Write the allocations to `/home/user/port_assignments.txt` in the format `Service: Port`, one per line, following the startup order.

**Test Data setup:**
Before writing your script, create the following test files to validate your solution.

`/home/user/services.deps`:
```text
auth: db
backend: auth cache
cache:
db:
frontend: backend auth
metrics: db
```

`/home/user/port_constraints.txt`:
```text
auth: 5000-5005
backend: 5000-5010
cache: 6379-6380
db: 5432-5433
frontend: 80-90
metrics: 5000-5005
```

Ensure your script `/home/user/resolve_env.sh` is executable and run it using the test data:
`./resolve_env.sh /home/user/services.deps /home/user/port_constraints.txt`