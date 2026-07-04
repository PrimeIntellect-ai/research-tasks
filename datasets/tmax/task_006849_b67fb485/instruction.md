You are a build engineer managing an artifact registry for a large software project. Your team is migrating metadata from a legacy CSV format to a new structured JSON schema to integrate with modern tooling. 

Additionally, the storage team has asked for a custom heuristic metric, the `storage_index`, to help bin-pack artifacts into different storage tiers, and they need a baseline performance benchmark of the migration process itself.

You have a CSV file located at `/home/user/artifacts/registry.csv` with the following header and format:
`id,timestamp,size_bytes,filename`

Your task is to create a Bash script at `/home/user/migrate.sh` that fulfills the following requirements:

1. **Schema Migration & Data Parsing**: Read the CSV file (ignoring the header) and convert it into a well-formed JSON array, saving the output to `/home/user/artifacts/new_registry.json`.
2. **Numerical Algorithm**: For each artifact, transform and calculate new fields:
    * `size_mb`: The `size_bytes` converted to megabytes (divide by 1048576). Format this strictly as a floating-point number with exactly two decimal places.
    * `storage_index`: An integer representing the storage tier. The formula is: `ceiling(sqrt(size_mb) * 1.5)`. (e.g., if `size_mb` is 47.68, sqrt is ~6.905, multiplied by 1.5 is ~10.357, ceiling makes it 11).
3. **JSON Structure**: The output JSON must be an array of objects, where each object looks exactly like this:
   ```json
   {
     "id": "art-1234",
     "filename": "build-output.tar.gz",
     "size_mb": 47.68,
     "storage_index": 11
   }
   ```
4. **Performance Benchmarking**: The script must measure the execution time of the CSV-to-JSON conversion process using the `/usr/bin/time` command. Specifically, capture the **user CPU time** (using the format string `"%U"`) and output *only* that numeric value to a new log file at `/home/user/artifacts/benchmark.log`. 
5. The script `/home/user/migrate.sh` must be marked as executable.

Write the complete script to solve this. Keep in mind that standard Bash utilities like `awk` and `jq` are available and well-suited for these transformations.