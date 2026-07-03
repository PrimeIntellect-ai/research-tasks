You are an engineer tasked with fixing a build determinism issue in our polyglot build system. 
We have multiple microservices defining HTTP routes in custom `.route` files. In our CI pipeline, merging these routes has become non-deterministic, causing unexpected test failures similar to import ordering bugs in Python.

Your task is to create a Rust CLI application from scratch that parses, merges, diffs, and deterministically outputs these routing definitions.

### Setup Requirements
1. Initialize a new Rust project at `/home/user/route-compiler` using `cargo`.
2. The route files to process are located in `/home/user/routes/` (you will need to process all `.route` files in this directory).
3. The previous build state is located at `/home/user/routes/previous.txt`.

### Input Format
Each line in a `.route` file represents one route and is space-separated:
`<METHOD> <PATH_WITH_QUERY_PARAMS> <HANDLER_NAME> <WEIGHT>`
Example:
`POST /login?method=oauth&retry=true login_handler 20`

### Processing Rules
1. **URL Parsing**: Extract the HTTP Method, Base Path (everything before `?`), and the Query Parameter Keys. Sort the query parameter keys alphabetically.
2. **Merging**: 
   - A route is uniquely identified by its `<METHOD>` and `<Base Path>`.
   - If multiple routes have the same Method and Base Path, keep the one with the highest `<WEIGHT>`.
   - If there is a tie in Weight, keep the route whose `<HANDLER_NAME>` comes first alphabetically.
3. **Sorting**: Sort the final merged list of routes first by Weight (Descending), then by Method (Ascending/Alphabetical), and finally by Base Path (Ascending/Alphabetical).
4. **Diffing**: Compare the final merged routes against the routes listed in `/home/user/routes/previous.txt`. Identify keys (`METHOD BasePath`) that were ADDED, REMOVED, or MODIFIED. A route is MODIFIED if its Handler, Weight, or sorted Parameter Keys differ from the previous build.

### Output Requirements
Your Rust program must execute and generate two files:

**1. `/home/user/merged.txt`**
Contains the deterministically merged and sorted routes.
Format: `<METHOD> <BasePath> [<sorted_param_key1>, <sorted_param_key2>] -> <HANDLER_NAME> (Weight: <WEIGHT>)`
Example: `POST /login [method, retry] -> login_handler (Weight: 20)`
*(Note: If there are no query parameters, output `[]`)*

**2. `/home/user/diff.txt`**
Contains the differences compared to `previous.txt`.
Format: `<STATUS>: <METHOD> <BasePath>`
Where `<STATUS>` is `ADDED`, `REMOVED`, or `MODIFIED`.
This file must be sorted alphabetically by `<METHOD>`, then by `<BasePath>`.

Write the Rust code, compile it, and run it to produce these files. Let me know when you've finished by explaining the commands you used.