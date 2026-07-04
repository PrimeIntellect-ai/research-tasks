You are tasked with building a configuration management ingestion pipeline. The system tracks configuration changes sent from distributed agents. You must write a C++ log normalizer, and configure the services that orchestrate the pipeline.

**Part 1: The C++ Normalizer**
Write a C++ program at `/home/user/normalizer` that reads a custom configuration patch from `stdin` and writes the normalized patch to `stdout`.

Patch Format:
Lines start with either `+ ` (add/update) or `- ` (remove), followed by a key, an equals sign `=`, and a value (for `+` only).
Example:
```
+ DB_HOST=localhost
- OLD_PORT
+ Greeting=Hello 🌍
```

Normalization Rules:
1. Validate that the entire input is valid UTF-8. If any invalid UTF-8 sequences are found, print `ERROR: INVALID_UTF8` to `stdout` and exit with code 1.
2. Extract the keys and values. Ignore empty lines or lines that do not strictly start with `+ ` or `- `.
3. Keys must be converted to lowercase ASCII.
4. For `+` entries, trim leading and trailing ASCII whitespace (` `, `\t`, `\n`, `\r`) from the value.
5. If a trimmed value exceeds 50 bytes in length, print `ERROR: LENGTH_EXCEEDED` and exit with code 1.
6. If the same key appears multiple times, the last valid operation in the input takes precedence.
7. Print the final state of operations sorted alphabetically by the lowercased key.
   Format for output:
   `[op] [key]=[value]` (for additions)
   `[op] [key]` (for removals)
   where `[op]` is `+` or `-`.

Compile your code to `/home/user/normalizer` (an executable). You may use standard C++17 or C++20 features. Do not use external libraries other than the standard library.

**Part 2: Service Composition**
We have three services that need to be wired together to complete the pipeline:
1. **Redis**: Needs to run on port `6379`.
2. **Flask API**: Provided at `/app/api.py`. It listens on `127.0.0.1:5000`. It receives HTTP POST requests with raw config patches, pipes them through your `/home/user/normalizer`, and saves the results to Redis.
3. **Nginx**: Must be configured to listen on `0.0.0.0:8080`. Any POST request to `http://127.0.0.1:8080/patch` must be proxied to the Flask API at `http://127.0.0.1:5000/ingest`.

Your Tasks for Part 2:
- Edit `/etc/nginx/nginx.conf` (or drop a conf in `/etc/nginx/sites-enabled/`) to set up the proxy rule. You have `sudo` privileges for nginx configuration, but run services as the `user` where possible.
- Ensure Redis is running and configured with `maxmemory 10mb`. You can create a redis config file at `/home/user/redis.conf` and start it.
- Start the Flask app using `python3 /app/api.py &`.
- Start or reload Nginx.

Make sure the end-to-end flow works: `curl -X POST --data-binary "+ KEY=val" http://127.0.0.1:8080/patch` should result in the Flask app returning 200 and storing the normalized patch in Redis.