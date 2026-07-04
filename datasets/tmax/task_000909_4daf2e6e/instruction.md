You are a web developer building a new micro-frontend feature. The feature consists of multiple interconnected modules that must be built and routed in a specific dependency order. 

Your task is to write a Bash script that performs dependency resolution (graph traversal) on these modules and generates a reverse proxy configuration snippet based on the resolved build order.

The modules are located in `/home/user/modules/`. Each module has its own directory containing a `deps.txt` file. The `deps.txt` file lists the names of other modules it depends on, one per line. If a module has no dependencies, its `deps.txt` will be empty.

Write a Bash script at `/home/user/generate_routes.sh` that does the following:
1. Scans `/home/user/modules/` to discover all modules and reads their `deps.txt`.
2. Performs a topological sort to resolve the dependency graph. 
3. In case of a tie (multiple modules have their dependencies met at the same time), resolve the tie by picking the module name that comes first alphabetically.
4. Generates an Apache-style reverse proxy configuration file at `/home/user/routes.conf`.
5. For each module, in the exact topologically sorted order, append a line to `/home/user/routes.conf` in this format:
   `ProxyPass /<module_name> http://localhost:8080/<module_name>`

For example, if the resolved order is `core`, then `auth`, the `/home/user/routes.conf` file should exactly be:
ProxyPass /core http://localhost:8080/core
ProxyPass /auth http://localhost:8080/auth

Constraints:
- You must write the solution entirely in Bash, using standard shell utilities (awk, grep, sed, sort, etc.). Do not use Python, Perl, or other scripting languages.
- The script must be executable.
- The final output file `/home/user/routes.conf` must perfectly match the expected ordered output.