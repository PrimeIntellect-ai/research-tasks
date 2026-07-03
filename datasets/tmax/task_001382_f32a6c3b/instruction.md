You are an integration developer setting up a test environment for a legacy API backend. The legacy system uses a custom string-based command protocol, and you need to build a mock server in Rust to test your API integration, alongside an Nginx reverse proxy to route traffic.

Your objective is to:
1. Create a Rust project at `/home/user/mock_api`. 
2. Write a raw HTTP server in Rust (using only `std::net`, no external HTTP crates like `hyper` or `actix-web`) that listens on `127.0.0.1:9000`.
3. The server must accept HTTP POST requests. The body of the request will contain a sequence of characters representing operations on a custom data structure (a tally of ASCII letters).
4. You must parse the body using a strict State Machine with the following logic:
   - The parser starts in an `Idle` state.
   - If it reads `+`, it transitions to `ExpectAdd`. The next character must be an uppercase ASCII letter (A-Z). It increments the tally for that letter, then returns to `Idle`.
   - If it reads `-`, it transitions to `ExpectSub`. The next character must be an uppercase ASCII letter. It decrements the tally for that letter (can be negative), then returns to `Idle`.
   - If it reads `?`, it transitions to `ExpectQuery`. The next character must be an uppercase ASCII letter. It records the current tally of that letter into an output buffer, then returns to `Idle`.
   - If any unexpected character is encountered (including invalid transitions or lowercase letters when uppercase is expected, but *ignoring* whitespace/newlines), the parser should immediately abort processing the rest of the string.
5. The HTTP response must be a standard `HTTP/1.1 200 OK` containing a plain text body. The body must be the comma-separated integer results of all `?` queries in the request. For example, if the queries resulted in 5, -1, and 0, the body should be `5,-1,0`.
6. Create an Nginx configuration file at `/home/user/nginx.conf`. It should run a server listening on `127.0.0.1:8080`.
7. The Nginx config must route any requests to the path `/legacy` to your Rust server at `http://127.0.0.1:9000`.
8. The Nginx config must also append a custom HTTP response header `X-Mock-Proxy: Active` to the proxied response.
9. Start your Rust server in the background, and then start Nginx using your custom config file (e.g., `nginx -c /home/user/nginx.conf`).

Leave both the Rust server and Nginx running. I will run an automated test that sends POST requests to `http://127.0.0.1:8080/legacy` to verify the state machine parser and proxy configuration.