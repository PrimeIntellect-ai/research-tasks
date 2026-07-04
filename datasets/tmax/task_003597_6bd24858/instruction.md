You are an engineer adapting a C++ web security log analyzer to run in a minimal container. The analyzer processes Nginx reverse proxy logs, decodes URL-encoded request paths, and compares them against known bad signatures.

You have the following files in `/home/user`:
1. `/home/user/url_tool.cpp`: A C++ utility that reads strings from standard input, URL-decodes them, and prints them. It also contains a skeletal `--test` flag for property-based testing.
2. `/home/user/access.log`: An Nginx access log containing requests with encoded payloads.
3. `/home/user/known_bad.txt`: A sorted list of decoded bad request paths.

Unfortunately, `url_tool.cpp` has a bug in its character decoding logic, and the minimal container needs an Nginx configuration file.

Please perform the following tasks:

1. **Fix the Encoding Bug & Implement Property-Based Testing:**
   - Find and fix the bug in the `decode_url` function inside `/home/user/url_tool.cpp`.
   - Complete the property-based testing logic in the `run_property_tests()` function. It must generate 1000 random alphanumeric strings (lengths 5 to 20), URL-encode them using the provided `encode_url` function, decode them using `decode_url`, and assert that the decoded string exactly matches the original. If any mismatch occurs, print an error and `exit(1)`. If all pass, print "PASS" and `exit(0)`.
   - Compile it to `/home/user/url_tool` using `g++ -O2 -std=c++17 /home/user/url_tool.cpp -o /home/user/url_tool`.

2. **Sort, Merge, and Diff the Logs:**
   - Extract just the request paths (the URL part of the HTTP request, e.g., `/admin?q=a`) from `/home/user/access.log`.
   - Pass these paths through your compiled `/home/user/url_tool` to decode them.
   - Sort the decoded paths and remove duplicates.
   - Use the `comm` command to find paths that are present in BOTH your sorted decoded paths AND `/home/user/known_bad.txt`.
   - Save these common (matching) paths to `/home/user/matches.txt`.

3. **Reverse Proxy Configuration:**
   - Create a minimal Nginx configuration file at `/home/user/proxy.conf`.
   - The config must run in the foreground (`daemon off;`), run as the current user (do not include a `user` directive), and store the pid in `/home/user/nginx.pid`.
   - Configure an `http` block with a `server` listening on `127.0.0.1:8080`.
   - It should route all requests (`location /`) to a reverse proxy backend at `http://127.0.0.1:9000`.
   - It must log accesses to `/home/user/access.log`.

Do not use root access or `sudo`. All tools (g++, awk, comm) are available in the container environment.