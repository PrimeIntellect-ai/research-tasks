You are an engineer tasked with porting a legacy Bash-based microservice to run in a minimal Linux container. This service acts as a simple dependency resolver behind a WebSocket interface. Currently, the service has a few critical bugs that prevent it from working correctly.

The system uses `websocat` to handle WebSocket connections, passing incoming text messages to a script located at `/home/user/app/handler.sh` via STDIN, and sending the script's STDOUT back to the client.

You need to fix `/home/user/app/handler.sh` to fulfill the following requirements:

1. **Parameter Parsing:** The script receives a string on STDIN like `RESOLVE /api/deps?verbose=1&pkg=database&format=text`. You must extract the value of the `pkg` query parameter. The parameter could appear anywhere in the query string.
2. **Dependency Resolution:** Once the package name is extracted, read the file `/home/user/app/packages.db`. The file format is `package_name: dep1 dep2 dep3`. You must recursively resolve all dependencies for the requested package.
3. **Sorting and Merging:** The final output should be a single space-separated string of all unique transitive dependencies, sorted alphabetically. It must be prefixed with `SUCCESS: ` (e.g., `SUCCESS: cache config logger network`). The requested package itself should not be in the output unless it is a dependency of one of its dependencies.
4. **Circular Dependency Detection:** The current script gets stuck in an infinite loop because `packages.db` contains circular dependencies (e.g., A depends on B, B depends on A). You must fix the recursive resolution logic to keep track of the visit path. If a circular dependency is detected during traversal, immediately halt and output exactly: `ERROR: cycle detected`.

**Initial State:**
The directory `/home/user/app/` contains:
- `packages.db`: The dependency database.
- `handler.sh`: The buggy script you need to fix.

Make sure your fixed `handler.sh` is executable and relies only on standard Bash built-ins and coreutils (awk, sed, grep, sort, etc.). Do not install any extra packages.

To verify your work, you can simulate a WebSocket message by piping a string into your script:
`echo "RESOLVE /api/deps?pkg=web_server" | ./handler.sh`