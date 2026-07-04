You are a release manager preparing a new software deployment. You need to automate the generation of a release manifest that calculates a mathematical "Risk Score" based on code diffs and compiles a summary of our newly exposed APIs.

There are two directories containing the source code for our hypothetical Rust project:
- `/home/user/project_v1/` (previous release)
- `/home/user/project_v2/` (current release)

Additionally, the developer has left an API specification file at `/home/user/project_v2/api_specs.txt`.

Your task is to write a bash script or use bash commands to perform the following steps and output a single JSON file at `/home/user/release_manifest.json`:

1. **Calculate the Risk Score:**
   - Generate a unified diff between `/home/user/project_v1/src/main.rs` and `/home/user/project_v2/src/main.rs` (using the standard `diff -u` command).
   - Count the total number of added lines ($A$) and deleted lines ($D$). *Note: Do not count the unified diff header lines starting with `+++` or `---`.*
   - Calculate the Risk Score ($R$) using the following formula: 
     $$R = (A \times 2) + (D \times 3) + ((A \times D) \bmod 7)$$

2. **Parse the API Specs:**
   - Read `/home/user/project_v2/api_specs.txt`.
   - Extract all REST endpoint paths (ignore the HTTP method, just get the path).
   - Extract all GraphQL types defined.

3. **Construct the Manifest Data:**
   - Create a structured JSON file at `/home/user/release_manifest.json` exactly matching this format:
     ```json
     {
       "risk_score": <calculated_R_as_integer>,
       "rest_endpoints": [
         "/path1",
         "/path2"
       ],
       "graphql_types": [
         "Type1",
         "Type2"
       ]
     }
     ```
   - Ensure the JSON is well-formed (you can use `jq` to format or construct it). The arrays should retain the order found in the text file.