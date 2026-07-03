You are a script developer tasked with building a web security utility that validates API gateway routing paths. We are migrating our microservice routing rules into a compiled C++ authorizer.

Phase 1: Architecture Extraction
We have provided an image of our reverse proxy routing architecture at `/app/sec_graph.png`. This image contains a text block detailing the valid microservice dependency graph (e.g., showing which service is allowed to call which other service). You must extract the directed graph rules from this image.

Phase 2: Polyglot Build & Utility
Write a C++ program at `/home/user/auth_checker.cpp` that acts as the core path validator. 
Your program must:
1. Hardcode or load the graph relationships extracted from the image.
2. Accept exactly one command-line argument: a URL-encoded string representing a requested execution path. The path will be a comma-separated list of service nodes (e.g., `%41%75%74%68%2C%57%41%46` which decodes to `Auth,WAF`).
3. Decode the input.
4. Verify if the requested path is a valid contiguous sequence in the dependency graph. 
5. Print strictly `ALLOW` if every hop in the sequence is valid according to the graph, or `DENY:<node>` where `<node>` is the first node in the sequence that violates the graph structure (or does not exist).
6. Create a `Makefile` in `/home/user/` to compile this C++ program to `/home/user/auth_checker` using `g++` with `-O3` and `-std=c++17`. Include a dummy target for a Go proxy build (you don't need to actually write the Go code, just create a target `proxy:` that echoes "Proxy built").

Ensure your C++ code correctly handles URL-decoding (including standard alphanumeric and special characters) before traversing the graph.