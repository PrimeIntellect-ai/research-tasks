You are a platform engineer maintaining our CI/CD systems. We need a fast pipeline validation tool to detect malformed or mathematically impossible pipeline configurations before they are scheduled.

Your task is to build a validator workflow consisting of a C program and a minimal REST API. 

**Step 1: Fix and Compile the Vendored cJSON library**
We vendor the `cJSON` library to parse pipeline definitions. The source is located at `/app/cjson-1.7.15/`. However, a recent configuration change broke its `Makefile`. You must fix the `Makefile` so that running `make` successfully produces `libcjson.so`.

**Step 2: Create a Resource Limits REST API**
Write a simple Python REST API (e.g., using `http.server` or `Flask`) that listens on `127.0.0.1:8080`. 
When it receives a `GET /limits` request, it must return exactly this JSON:
`{"max_cpu": 100, "max_mem": 200}`
Start this server in the background so it is available for Step 3.

**Step 3: Build the C Validator (`ci_validator`)**
Write a C program located at `/home/user/ci_validator`. 
Usage: `/home/user/ci_validator <path_to_pipeline.json>`

The validator must:
1. Fetch the resource limits by making an HTTP GET request to `http://127.0.0.1:8080/limits` (you may use sockets, `libcurl`, or `popen` with `curl`).
2. Parse the target pipeline JSON file using the fixed `libcjson.so`.
3. Check the pipeline against these constraint satisfaction rules:
   - **Math/Resource Constraint**: The sum of `cpu` for all jobs in the pipeline must NOT exceed `max_cpu`, and the sum of `mem` must NOT exceed `max_mem`.
   - **Dependency Constraint**: The `depends_on` arrays for the jobs must NOT contain any cyclic dependencies. (e.g., Job A depends on Job B, and Job B depends on Job A).
4. If ALL constraints are satisfied, the program must terminate with exit code `0`.
5. If ANY constraint is violated (or if the file is invalid), it must terminate with a non-zero exit code (e.g., `1`).

**Input Format:**
The pipeline JSON files look like this:
```json
{
  "jobs": [
    {
      "name": "build",
      "cpu": 40,
      "mem": 80,
      "depends_on": []
    },
    {
      "name": "test",
      "cpu": 50,
      "mem": 100,
      "depends_on": ["build"]
    }
  ]
}
```

Ensure your `ci_validator` compiles successfully, linking against the vendored `cJSON` library. We will test your binary against a corpus of clean and evil pipeline JSONs.