You are a web developer building a lightweight feature for a build dashboard. We need a simple API endpoint written entirely in **Bash** that calculates if a set of requested shared libraries will fit into a given memory constraint, acting as a rudimentary dependency constraint checker. 

Create an executable Bash script at `/home/user/solver.sh`. 

The script must act as a CGI-style script. It will receive a raw HTTP GET request on `stdin` and must output a valid HTTP response to `stdout`.

**Requirements:**
1. **URL Routing & Parameter Parsing:**
   The script should accept HTTP GET requests. The request line will look like:
   `GET /api/v1/fit?libs=core,math,net,ui&max=150 HTTP/1.1`
   - You only need to handle the `/api/v1/fit` route. If a different route is provided, return an `HTTP 404 Not Found` response with an empty body.
   - Parse the `libs` parameter (a comma-separated list of library names) and the `max` parameter (an integer).

2. **Data Lookup (Schema):**
   Read from a CSV file located at `/home/user/libs.csv`. Each line has the format `library_name,size_in_kb` (e.g., `math,45`). Ignore any requested libraries that do not exist in the CSV.

3. **Numerical & Constraint Logic:**
   - Find the sizes of all requested libraries that exist in the CSV.
   - Calculate their total sum.
   - Check the constraint: Does the total sum exceed the `max` parameter?

4. **REST API Construction (Output format):**
   - If the sum exceeds `max`, return an `HTTP 400 Bad Request` with the following exact JSON body:
     `{"error": "exceeds capacity", "total": <SUM>, "max": <MAX>}`
   - If the sum is less than or equal to `max`, return an `HTTP 200 OK` with the following exact JSON body:
     `{"status": "ok", "total": <SUM>}`
   - *Ensure your HTTP response includes the correct status line, a `Content-Type: application/json` header, a blank line separating headers from the body, and the JSON string.*

**Example CSV (`/home/user/libs.csv`):**
```
core,50
math,30
net,25
```

**Example execution:**
```bash
echo -e "GET /api/v1/fit?libs=core,net&max=100 HTTP/1.1\r\nHost: localhost\r\n\r\n" | ./solver.sh
```
**Expected Output:**
```
HTTP/1.1 200 OK
Content-Type: application/json

{"status": "ok", "total": 75}
```

Write the robust Bash script to satisfy these constraints.