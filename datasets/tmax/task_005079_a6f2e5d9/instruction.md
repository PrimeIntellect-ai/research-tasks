You are assisting a compliance officer who is auditing our systems for transaction deadlocks and financial anomalies. We use a custom query generation library to build MongoDB aggregation pipelines for our audit reports, but our infrastructure recently suffered a configuration loss. 

We have a vendored package called `mongogen-audit` located at `/app/mongogen-audit-0.5.0`. It is supposed to compile JSON audit rules into MongoDB aggregation pipelines. However, there is a bug in the package: when constructing complex joins (`$lookup` stages), it incorrectly hardcodes the local field to `"_id"` instead of using the dynamically provided local field. 

Your tasks are as follows:

1. Locate and fix the bug in the vendored `mongogen-audit` package at `/app/mongogen-audit-0.5.0`. The library is already in the Python path for the environment.
2. Create a Python script at `/home/user/build_pipeline.py` that takes a single command-line argument containing a JSON string.
3. The JSON string will have the following schema:
   ```json
   {
     "source_collection": "<string>",
     "match_status": "<string>",
     "join_collection": "<string>",
     "join_local_field": "<string>",
     "join_foreign_field": "<string>",
     "join_as": "<string>",
     "fields": ["<string>", "<string>"]
   }
   ```
4. Your script must parse this JSON and use the `mongogen.compiler.PipelineBuilder` class from the fixed package to construct a NoSQL aggregation pipeline.
   - Initialize the builder with the `source_collection`.
   - Add a match stage for `{"status": "<match_status>"}`.
   - Add a lookup (join) stage using the provided `join_collection`, `join_local_field`, `join_foreign_field`, and `join_as`.
   - Add a projection stage for the array of `fields`.
5. The script must print the resulting MongoDB aggregation pipeline as a fully formatted JSON string to standard output (using the builder's `to_json()` method).
6. Ensure your script handles edge cases gracefully, as it will be rigorously tested against a large number of randomly generated JSON inputs representing different compliance audit rules.

Your final deliverable is the fixed package and the `/home/user/build_pipeline.py` script. The verification system will fuzz your script with hundreds of randomized inputs to ensure it is bit-exact equivalent to our reference compliance oracle.