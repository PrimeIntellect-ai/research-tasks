You are a QA engineer responsible for setting up a local test environment for a complex microservice architecture. To route traffic correctly during integration testing, we use a dynamic reverse proxy.

The services and their dependencies are defined in a custom Domain Specific Language (DSL) located at `/home/user/mesh.dsl`. 
Each line in this file specifies a dependency in the format `ServiceA -> ServiceB`, meaning "Service A depends on Service B". If a service has no dependencies, it is written as `ServiceX -> NONE`.

Your task is to write a Go program at `/home/user/build_env.go` that acts as an interpreter for this DSL. Your program must:
1. Read and parse `/home/user/mesh.dsl`.
2. Perform a graph traversal to resolve the dependencies and determine the correct startup order (topological sort).
3. Assign a local HTTP URL to each service, starting with `http://localhost:8000` and incrementing the port number by 1 for each service in the startup sequence.
4. To ensure deterministic output, if multiple services have their dependencies satisfied at the same time, process and assign their ports in alphabetical order.
5. Generate a reverse proxy routing table as a JSON file at `/home/user/proxy_config.json`. The JSON should be a flat key-value map where the key is the service name and the value is the assigned URL string.

Example DSL:
```
Frontend -> Backend
Backend -> Database
Database -> NONE
Logger -> NONE
```

Example output format for `proxy_config.json` (note the alphabetical resolution for ties):
```json
{
  "Database": "http://localhost:8000",
  "Logger": "http://localhost:8001",
  "Backend": "http://localhost:8002",
  "Frontend": "http://localhost:8003"
}
```

Write the Go program, compile or run it, and ensure `/home/user/proxy_config.json` is generated correctly based on the actual contents of `/home/user/mesh.dsl`. Do not assume the contents of `mesh.dsl` match the example above.