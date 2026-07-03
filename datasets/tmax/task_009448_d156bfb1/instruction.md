You are tasked with building a lightweight, Bash-based HTTP API request handler for organizing and evaluating project files. As a developer, you need a quick way to query file metadata and evaluate custom metrics without installing external language runtimes like Python or Node.js.

Write a Bash script at `/home/user/api.sh` that simulates handling REST API requests. It must accept the HTTP METHOD as the first argument, the URI path (including query strings) as the second argument, and read any HTTP request body from standard input (`stdin`). 

Your script must target files located in the `/home/user/src` directory.

The script must handle the following two endpoints and print a valid HTTP response (headers and body) to standard output (`stdout`).

**1. GET /files?ext=<extension>**
- Returns a JSON list of filenames inside `/home/user/src` that match the given extension.
- Do not include the directory path in the filenames.
- Example execution: `/home/user/api.sh GET /files?ext=txt`
- Example output:
```
HTTP/1.1 200 OK
Content-Type: application/json

{"files": ["readme.txt", "notes.txt"]}
```

**2. POST /evaluate**
- Reads a raw text expression from `stdin`.
- The expression represents a custom metric calculation using file statistics. It may contain basic arithmetic operators (`+`, `-`, `*`, `/`, spaces) and two custom functions:
  - `SIZE(filename)`: Evaluates to the size of the file in bytes.
  - `LINES(filename)`: Evaluates to the total number of lines in the file.
- Your script must parse this custom expression, replace the functions with their actual numeric values for the files in `/home/user/src`, evaluate the final mathematical expression, and return the integer result in JSON.
- Example stdin: `SIZE(app.py) + LINES(utils.py) * 10`
- Example output:
```
HTTP/1.1 200 OK
Content-Type: application/json

{"result": 450}
```

**Constraints & Requirements:**
- You must write this entirely in Bash (`/home/user/api.sh`). Standard Linux CLI utilities (like `wc`, `stat`, `bc`, `grep`, `sed`, `awk`) are fully permitted.
- Ensure your script correctly outputs the exact HTTP headers shown above, followed by a blank line, followed by the JSON body.
- Return `HTTP/1.1 404 Not Found` (with an empty body) for any unrecognized endpoint or HTTP method.
- Return `HTTP/1.1 400 Bad Request` if a file referenced in a `SIZE` or `LINES` function does not exist in `/home/user/src`.
- Do not start a long-running web server daemon (like `netcat` or `socat`). The script should just process the inputs provided via arguments/stdin, print the response, and exit.
- Be sure to `chmod +x /home/user/api.sh`.