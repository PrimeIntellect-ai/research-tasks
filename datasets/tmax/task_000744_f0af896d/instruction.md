You are a QA engineer responsible for setting up a web security test environment. We are migrating a legacy Python-based token sanitizer to C++ for performance, and need to properly configure our test environment's reverse proxy to handle REST and WebSocket traffic.

Your task has two parts:

**Part 1: Code Translation (C++)**
There is a reference Python script at `/app/src/sanitizer.py` that takes an input string from `stdin`, applies a specific security sanitization algorithm (removing certain unsafe characters, normalizing case, and appending a checksum), and prints the result to `stdout`. 

You must translate this logic into a C++ program.
1. Create your C++ source file at `/home/user/workspace/sanitizer.cpp`.
2. Compile it to `/home/user/workspace/sanitizer` using `g++ -O3 sanitizer.cpp -o sanitizer`.
3. Your compiled C++ program must behave **exactly** like the reference Python script for any arbitrary string input. It will be aggressively fuzz-tested against a pre-compiled oracle binary.

**Part 2: Multi-Service Environment Configuration**
We use Nginx as a reverse proxy for our REST APIs and WebSocket services. The configuration file skeleton is located at `/home/user/workspace/nginx.conf`.
You need to complete the Nginx configuration so that when Nginx listens on port 8080:
1. All HTTP requests to `/api/` are routed to our Flask backend on `127.0.0.1:5000`.
2. All WebSocket connections to `/stream/` are routed to our WebSocket backend on `127.0.0.1:5001`. Make sure to include the necessary `Upgrade` and `Connection` headers for WebSockets to work.
3. Both upstreams should preserve the original `Host` header.

You do not need to start the Nginx, Flask, or WebSocket servers. Our automated test harness will launch them using your Nginx configuration to verify the end-to-end data flow.

Ensure your final C++ binary is located exactly at `/home/user/workspace/sanitizer` and your Nginx config is at `/home/user/workspace/nginx.conf`.