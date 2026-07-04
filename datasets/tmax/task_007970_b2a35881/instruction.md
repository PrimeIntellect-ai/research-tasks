You are a database administrator tasked with optimizing a graph database query and automating the export of its results. 

In your home directory (`/home/user`), you will find the following files:
1. `data.ttl` - A graph dataset in Turtle (RDF) format containing movie and actor relationships.
2. `slow_query.rq` - A SPARQL query that retrieves the names of all actors who co-starred with "KevinBacon". The current query is highly inefficient because it performs a Cartesian join on all movies (`?m1` and `?m2`) and then filters for equality, which is causing query planner timeouts on our larger production dataset.
3. `query_runner.py` - A provided Python script that executes a given SPARQL query against a Turtle file and outputs the standard SPARQL JSON results format to standard output. Usage: `python3 query_runner.py <data_file> <query_file>`

Your tasks are:
1. **Optimize the Query**: Analyze `slow_query.rq` and the schema in `data.ttl`. Write an optimized equivalent query and save it to `/home/user/fast_query.rq`. The optimized query must eliminate the Cartesian join (do not select two separate movie variables `?m1` and `?m2` and filter them to be equal). Instead, directly match the same movie node for both actors. It must return exactly the same `?coStarName` results.
2. **Export and Convert**: Write a Bash script at `/home/user/export_results.sh` that:
   - Uses `python3 query_runner.py data.ttl fast_query.rq` to execute your optimized query.
   - Pipes the JSON output to `jq` to extract the `value` of the `coStarName` bindings.
   - Formats the output as a CSV file saved to `/home/user/results.csv`.
   - The CSV file must have exactly one header column: `Actor`.
   - The actor names must be sorted alphabetically.
   - Do not include quotes around the actor names in the CSV.

Make sure your Bash script is executable and completely self-contained. The final verification will run your Bash script and check the contents of `/home/user/results.csv` and the structure of `/home/user/fast_query.rq`.