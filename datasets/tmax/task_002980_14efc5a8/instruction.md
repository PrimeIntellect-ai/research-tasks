You are a Database Administrator specializing in graph databases. Your team relies on a proprietary, internally developed graph query engine called `gq_engine` to process hierarchical queries and graph traversals. Recently, there have been issues with "query plan explosions" where poorly constructed recursive queries exhaust system memory, and a botched release of the engine has broken the parsing logic.

Your task consists of two phases:

**Phase 1: Fix the Vendored Package**
A pre-vendored source of `gq_engine` (version 1.0.4) is located at `/app/gq_engine-1.0.4`. It contains the logic for parsing and generating execution plans for our graph query JSON format. 
Currently, if you try to run any recursive query generation using `from gq_engine.planner import QueryPlanner`, it crashes. A junior developer hardcoded a configuration that broke it. 
You must investigate the vendored package, identify the perturbation that is breaking the query planner (specifically related to recursion limits configuration), fix it, and install the package locally in your environment. DO NOT try to download it from the internet.

**Phase 2: Build a Query Validator**
We need a robust filter to block malicious or overly expensive queries before they hit the database. You must write a Python CLI script at `/home/user/validate.py` that takes a JSON query file path as an argument.

Usage: `python /home/user/validate.py --file <path_to_json_file>`

The script must:
1. Read the JSON file.
2. Use the fixed `gq_engine.planner.QueryPlanner` to parse the JSON and get the `plan` object.
3. Determine if the query is safe ("clean") or malicious/expensive ("evil").
   A query is considered EVIL and must be REJECTED (exit code `1`) if ANY of the following are true:
   - The `plan.estimate_cost()` returns a value greater than `5000`.
   - The traversal path defined in the query contains a cycle (a repeated node label in the `restricted_path` list, if present).
   - The `max_depth` parameter exceeds `10`.
4. If the query is CLEAN, the script must ACCEPT it (exit code `0`).

Your solution will be tested against two hidden directories of queries: a "clean" corpus and an "evil" corpus. To succeed, your script must exit `0` for 100% of the clean queries and exit `1` for 100% of the evil queries. Ensure your code handles missing keys gracefully (e.g., if `restricted_path` is not provided, it's not a cycle).