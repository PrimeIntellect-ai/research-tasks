You are a script developer tasked with creating a testing utility for a newly developed, high-performance C-based URL router. 

The project is located in `/home/user/router_project/`. It contains the following files:
1. `router.c` - A C program that takes a URL as a command-line argument, parses the routing path and query parameters, and outputs a custom string format: `ROUTE:[path]|PARAMS:[key=value,key=value]|VALID:[1 or 0]`.
2. `Makefile` - A makefile to build the C program.
3. `urls.txt` - A file containing a list of URLs to test (one per line).

However, the project currently has issues:
1. The `Makefile` is broken and fails to build the executable.
2. The `router.c` program has a bug where it crashes (segmentation fault) when parsing certain valid URLs.

Your task is to:
1. **Fix the Makefile**: Ensure it correctly compiles `router.c` into an executable named `url_router` in the same directory.
2. **Debug and fix `router.c`**: Identify and fix the segmentation fault so it can handle all URLs in `urls.txt` without crashing. It must correctly output the format `ROUTE:<path>|PARAMS:<query_string>|VALID:1`. If there are no query parameters, it should output `PARAMS:none`.
3. **Write a test utility**: Create a script in any language you choose (e.g., Python, Bash, Node.js) named `test_runner.*` (e.g., `test_runner.py`) in `/home/user/router_project/`.
   - The script must read `urls.txt`.
   - It must execute `./url_router <url>` for each line.
   - It must parse the custom string output from the C program.
   - Finally, it must generate a JSON report at `/home/user/router_project/report.json`.

The `report.json` must exactly match this custom data structure schema:
```json
{
  "total_tested": <int>,
  "successful_executions": <int>,
  "results": [
    {
      "original_url": "<string>",
      "parsed_route": "<string>",
      "parsed_params": "<string>"
    }
  ]
}
```
*Note: `parsed_params` should be exactly the string extracted from the `PARAMS:[...]` block (e.g., `id=5&sort=asc` or `none`).*

Ensure that your `report.json` is accurately formatted and generated successfully after running your test utility.