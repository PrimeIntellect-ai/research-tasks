You are an engineer porting our C++ edge routing system into a new minimal container environment. Before we migrate the full WebSocket proxy server, we need to extract and rewrite its URL routing security filter as a standalone C++ utility. We want to ensure it is robust against malformed WebSocket requests and doesn't introduce memory leaks, as the previous version crashed frequently under load.

Your task is to write this standalone C++ sanitizer program. 

We had a whiteboard session defining the exact security rules for incoming WebSocket connections. A photograph of the whiteboard has been placed in your environment at `/app/ws_rules.png`. You will need to extract the text from this image to understand the routing rules you must implement.

Write a C++ program at `/home/user/url_sanitizer.cpp` that acts as our filter. 
The program must:
1. Accept a single URL string as its first command-line argument (`argv[1]`).
2. Parse the URL, applying the routing constraints and parameter validations specified in the whiteboard image.
3. Exit with status code `0` (and optionally print "ALLOW") if the URL strictly adheres to all rules.
4. Exit with status code `1` (and optionally print "DENY") if the URL violates any rule, is malformed, or is missing required routing parameters.
5. Be completely memory-safe. 

When we test your code, our automated build system will compile it with AddressSanitizer enabled:
`g++ -std=c++17 -O2 -fsanitize=address -Wall /home/user/url_sanitizer.cpp -o /home/user/sanitizer`

Our CI pipeline will then run the compiled binary against two distinct corpora of URLs (clean and malicious). Your program must perfectly classify them without triggering any memory leaks or ASAN errors.