You are an integration developer building a microservice orchestration planner. 

We need a system that takes a set of API calls (tasks), their computational costs, and their dependencies (which task must run before which), and schedules them into sequential execution batches such that no batch exceeds a specific maximum cost, and dependencies are respected.

Your objective is to complete the following multi-stage workflow:

1. **Fix the Vendored Package**:
   We vendor our dependencies. A specific version of `networkx` is located at `/app/vendored/networkx-2.8.8`. However, another developer accidentally introduced a syntax error in `/app/vendored/networkx-2.8.8/networkx/algorithms/dag.py` right at the start of the `lexicographical_topological_sort` function. You must find and fix this error so the package can be used. Ensure your `PYTHONPATH` includes `/app/vendored/networkx-2.8.8` when running your code.

2. **Build the Planner API**:
   Write a Flask REST API in `/home/user/server.py`. 
   - It should listen on port `5000`.
   - It must expose a `POST /plan` endpoint.
   - The endpoint expects a JSON payload: `{"data": <input_json>}`.
   - The `<input_json>` is a string representing a JSON object with this schema:
     ```json
     {
       "tasks": {
         "TaskA": {"cost": 5},
         "TaskB": {"cost": 10},
         "TaskC": {"cost": 2}
       },
       "dependencies": [
         ["TaskA", "TaskB"], 
         ["TaskA", "TaskC"]
       ],
       "max_cost_per_batch": 12
     }
     ```
     *(Note: `dependencies` is a list of `[source, destination]` pairs, meaning `source` must be completed before `destination`.)*
   - **Scheduling Logic**:
     - Perform a lexicographical topological sort (resolve dependencies). If multiple tasks are ready to be scheduled, prioritize them alphabetically by task name.
     - Group the sorted tasks into batches (arrays of task names).
     - Iterate through the sorted tasks and add them to the current batch as long as the sum of their costs does not exceed `max_cost_per_batch`.
     - If adding the next task exceeds the limit, start a new batch.
     - Return the batches as a JSON array of arrays (e.g., `[["TaskA", "TaskC"], ["TaskB"]]`).
   - Run this server in the background.

3. **Create the CLI Wrapper for Benchmarking/Testing**:
   Write a Python script `/home/user/request_planner.py` that takes a single command-line argument (the raw JSON string of tasks, exactly as defined in `<input_json>`).
   - The script must make an HTTP POST request to `http://localhost:5000/plan` passing the JSON string inside the `{"data": ...}` wrapper.
   - The script must print *only* the resulting JSON array of batches to `stdout` and exit.

**Verification:**
An automated suite will test your implementation by running `/home/user/request_planner.py` with hundreds of randomly generated DAGs and constraints to verify bit-exact behavioral equivalence with a reference oracle.