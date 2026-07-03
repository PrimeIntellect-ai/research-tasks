As a database administrator, you are tasked with protecting your graph database from overly expensive projection and materialization queries. 

You are provided with a proprietary, compiled query planning tool located at `/app/query_planner`. It reads a query string from standard input and outputs a JSON representation of the query execution plan to standard output. 

You must write a Bash wrapper script at `/home/user/gatekeeper.sh` that implements a query-to-pipeline chaining mechanism. The script must take a single argument: the path to a file containing a query.

Your script must perform the following:
1. Read the query from the specified file.
2. Pass the query into `/app/query_planner` via stdin.
3. Parse the resulting JSON execution plan. The JSON contains a recursive tree of query operators. Each operator may have an `est_cost` (integer) field and an `inputs` (array) field containing child operator objects.
4. Calculate the total estimated cost of the query by summing the `est_cost` values of all operators across the entire deeply nested tree.
5. Apply filtering: If the total cost is strictly greater than 5000, the script must reject the query by exiting with status code 1.
6. If the total cost is 5000 or less, the script must accept the query by exiting with status code 0.

Ensure your script is executable and robust enough to handle arbitrarily deep JSON trees using command-line tools like `jq`.