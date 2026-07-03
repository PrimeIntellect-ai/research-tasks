You are a mobile build engineer maintaining our next-generation build pipeline. We are transitioning to a new internal domain-specific language (DSL) called `.buildflow` to define build steps and their dependencies. 

We have a multi-service setup located in `/app/`. Redis is already running on `127.0.0.1:6379` to store build pipeline configurations. 
Your task is to implement the core logic in `/app/build_service.py` using Python (Flask and redis-py are pre-installed).

The service must run on `127.0.0.1:5000` and expose a REST API to parse the DSL, detect circular dependencies (which currently break our CI), and save the valid build execution plan to Redis.

### DSL Format
The `.buildflow` language consists of lines defining steps and their requirements.
- `STEP <name>` defines a new build step.
- `REQUIRES <name>` (zero or more) immediately following a `STEP` indicates dependencies.

Example:
```
STEP compile_app
REQUIRES generate_code
REQUIRES fetch_assets
STEP fetch_assets
STEP generate_code
```

### API Requirements

1. **`POST /api/v1/builds`**
   - **Payload**: JSON `{"flow": "<multi-line string of DSL>"}`
   - **Logic**: 
     - Build a state machine/parser to read the DSL into a directed graph.
     - Detect if there are circular dependencies (e.g., A requires B, B requires A).
   - **Response (Cycle Detected)**: HTTP 400 Bad Request, with JSON `{"error": "circular dependency detected"}`.
   - **Response (Valid)**: 
     - Generate a random UUID string for `build_id`.
     - Compute the topological sort of the graph (a valid sequential execution order where dependencies come before the steps that require them). If multiple valid orders exist, any valid topological sort is acceptable.
     - Serialize this list of steps and store it in Redis under the key `build:<build_id>`.
     - Return HTTP 200 OK, with JSON `{"build_id": "<uuid>"}`.

2. **`GET /api/v1/builds/<build_id>`**
   - **Logic**: Retrieve the execution plan from Redis.
   - **Response**: HTTP 200 OK, with JSON `{"steps": ["fetch_assets", "generate_code", "compile_app"]}`. (Return 404 if not found).

Implement `/app/build_service.py` to meet these requirements, and then start the service in the background so it binds to `127.0.0.1:5000`. Leave the service running when you are finished.