You are tasked with porting an older bash/jq-based security auditing tool to a standalone Go binary so that it can run inside a minimal (distroless/scratch) container environment for web security scanning.

The tool analyzes a web service's dependency graph, evaluates vulnerability rules against the packages, and outputs a list of newly affected top-level applications.

Here is what you need to build:
Write a Go program at `/home/user/audit.go` and compile it. The program must perform the following tasks without relying on external system binaries (like `jq` or `sort`):

1. **Deserialize the Dependency Graph**: Read `/home/user/deps.json`. This file contains a directed graph of dependencies.
   - `nodes` have an `id`, `type` (either "app" or "lib"), `name`, and `version` (strictly in `X.Y.Z` format, e.g., `1.2.3`).
   - `edges` have a `from` and `to` field, meaning the node `from` depends on the node `to`.

2. **Evaluate Vulnerability Rules**: Read `/home/user/rules.txt`. 
   - Each line contains a vulnerability rule in the exact format: `<package_name> < <version>` (e.g., `lib-crypto < 2.2.0`).
   - You must parse these simple expressions and evaluate them against the nodes. Note that version comparisons must be numeric (e.g., `1.10.0` is greater than `1.9.0`).

3. **Graph Traversal**: 
   - A node is considered "vulnerable" if it matches any of the parsed vulnerability rules.
   - An "app" node is considered "affected" if it depends *directly or transitively* on any vulnerable node.

4. **Diffing and Sorting**:
   - Read `/home/user/baseline.txt`, which contains a newline-separated list of `id`s for applications that are *already known* to be vulnerable.
   - Compare your discovered "affected apps" against the baseline.
   - Output the `id`s of the *newly* affected apps (affected apps that are NOT in the baseline).
   - The output must be sorted alphabetically and written to `/home/user/new_vuln_apps.txt`, with one `id` per line.

Constraints:
- Use only the Go standard library.
- The versions are strictly in `X.Y.Z` format where X, Y, and Z are integers.

Ensure your code is correct and produces the exact output required in `/home/user/new_vuln_apps.txt`.