You are an engineer building a lightweight, Bash-based webhook router and build dependency resolver for our internal CI system. 

Our CI webhook receives URL paths representing a build request, such as `/build/frontend?env=prod` or `/build/api`. We need a Bash script that routes these requests, parses out the exact target, and calculates the correct build order based on a simple dependency graph file.

Create an executable Bash script at `/home/user/build_router.sh`.
The script will receive the URL path as its first and only argument.

Your script must perform the following steps:
1. **URL Routing & Parsing:** Extract the target name from the URL path. The URL will always start with `/build/`. Ignore any query parameters. For example, `/build/api?debug=true` should resolve to the target `api`.
2. **Graph Traversal (Dependency Resolution):** Read the dependency graph from `/home/user/deps.txt`. Each line in this file follows the format `target: dep1 dep2 ...` (space-separated). 
3. **Build Execution Output:** Calculate the build order for the requested target using a depth-first, post-order traversal (process dependencies left-to-right). A dependency must be built before the target that depends on it. Crucially, **do not build any target more than once**.
4. **Output Format:** For each target in the resolved build order, append the exact string `[BUILD] <target>` to a log file located at `/home/user/build_order.log`.

For example, if `deps.txt` contains:
```
app: libA libB
libA: core
libB: core
core:
```
And the script is executed with `/home/user/build_router.sh "/build/app"`, the `/home/user/build_order.log` should contain exactly:
```
[BUILD] core
[BUILD] libA
[BUILD] libB
[BUILD] app
```

Set up the script, ensure it has executable permissions (`chmod +x`), and test it. Do not execute it in your final step, just leave the script perfectly written.