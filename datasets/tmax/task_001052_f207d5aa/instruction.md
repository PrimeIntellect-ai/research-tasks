You have just inherited an unfamiliar data processing codebase. The core of this system is a script that extracts and aggregates structured data from JSON files using JMESPath queries. 

However, there is a major issue: the data engineering team has reported that queries involving array length, aggregations, or searches (like `contains`) are returning corrupted or incorrect results in production. 

The system relies entirely on a vendored copy of the `jmespath` Python library, which is located at `/app/vendored/jmespath-1.0.1`. The previous developer made some unauthorized and undocumented "optimizations" to this vendored library, which are likely the root cause of these issues.

Your objectives:
1. **Error Diagnosis & Root Cause Analysis**: Debug the vendored `jmespath` package in `/app/vendored/jmespath-1.0.1/` to find the undocumented changes causing incorrect query results.
2. **Intermediate State Tracing**: Trace how the functions are evaluating queries and isolate the exact functions in the library that have been modified.
3. **Fix the Package**: Repair the vendored `jmespath` library so that it correctly implements the JMESPath specification.
4. **Integration**: Create the entry-point script `/home/user/query.py`. This script must:
   - Run using `python3`.
   - Ensure the vendored package is at the front of `sys.path` so it uses `/app/vendored/jmespath-1.0.1/` and not any system-installed version.
   - Accept exactly two positional arguments: the path to a JSON file, and a JMESPath query string.
   - Print the exact JSON-encoded result of the query to standard output (no extra spaces, no pretty-printing, just `json.dumps(result, separators=(',', ':'))`).

To assist you with regression testing, there is a compiled reference binary at `/app/oracle_query`. This oracle exhibits the perfectly correct, known-good behavior. You can use it to build regression tests or do delta debugging against your script. 

Example usage of your script and the oracle:
```bash
python3 /home/user/query.py test.json "length(my_array)"
/app/oracle_query test.json "length(my_array)"
```

Once you are confident in your fix, automated tests will verify your `/home/user/query.py` by fuzzing it with thousands of random JSON documents and complex queries, asserting bit-exact output equivalence against `/app/oracle_query`.