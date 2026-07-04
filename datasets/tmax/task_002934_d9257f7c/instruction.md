You are an infrastructure engineer automating the provisioning of user web applications. Our stack uses Nginx as a reverse proxy to user-specific Gunicorn instances communicating over Unix domain sockets. We are currently facing two distinct problems that you must resolve.

**Part 1: The 502 Bad Gateway / Broken Vendored Package**
We vendor our own build of Gunicorn at `/app/gunicorn`. Recently, a bad patch was applied that breaks Unix socket binding. When users try to bind using `--bind unix:/tmp/app.sock`, Gunicorn internally binds to the wrong path, causing Nginx to return a 502 Bad Gateway because the socket doesn't exist where Nginx expects it.
Your task is to identify the perturbation in the source code under `/app/gunicorn` (specifically related to how the `unix:` prefix is parsed and sliced in the socket configuration module) and fix it. 

**Part 2: Upstream Configuration Generator**
To automate user provisioning, we need a script that generates NGINX upstream blocks based on active users and their disk quota usage. Users who exceed their disk quota (1,048,576 bytes) must have their upstream server marked as `down` to disable access until they free up space.

We have an existing compiled binary oracle at `/app/oracle_gen` which does this perfectly, but we are migrating to Python. 
Write a Python script at `/home/user/gen_upstreams.py` that reads a JSON payload from `stdin` and prints the exact NGINX configuration block to `stdout`.

The JSON input will be a list of dictionaries with the following keys:
- `user` (string): The username.
- `sock` (string): The absolute path to the unix domain socket.
- `quota_used` (integer): The user's current disk usage in bytes.

The output must exactly match the output of `/app/oracle_gen` byte-for-byte for any valid JSON input. You can test your script against the oracle by passing identical JSON to both.

Example output format expected from your script:
```nginx
upstream backend_alice {
    server unix:/tmp/alice.sock;
}
upstream backend_bob {
    server unix:/tmp/bob.sock down; # Quota exceeded
}
```
*(Note: Keep the exact spacing, newlines, and capitalization as produced by the oracle).*

Make sure your script handles an empty list by printing nothing, and processes the users in the exact order they appear in the JSON.