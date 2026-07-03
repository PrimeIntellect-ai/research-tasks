I am migrating an old web service from Python 2 to Python 3. As part of this migration, we are moving the security-critical authentication token generator out of Python completely and rewriting it in C++ for better performance and to serve as a standalone CGI-like binary for our internal REST API.

Here is the legacy Python 2 script that generates our custom web security tokens. It takes a username and a timestamp, and applies a custom numerical algorithm to generate a numeric token:

```python
# legacy_auth.py
def generate_token(username, timestamp):
    val = 0
    for i, char in enumerate(username):
        val += ord(char) * (i + 1)
    
    # Python 2 long integer multiplication
    # Modulo a large prime
    token = (val * long(timestamp)) % 999983
    return token
```

Your task is to write a C++ program at `/home/user/auth_api.cpp` that translates this logic and acts as a basic REST API backend. 

Requirements for the C++ program:
1. It must be written in `/home/user/auth_api.cpp`.
2. It should accept exactly one command-line argument in the structured format: `username:timestamp` (e.g., `./auth_api admin:1700000000`). You will need to parse this string to extract the username and timestamp.
3. It must implement the exact same numerical algorithm as the Python 2 code. Beware of integer overflow; ensure you use appropriate C++ data types for large timestamps.
4. It must output a raw HTTP REST response to `stdout`. The output must exactly match this format (including the blank line separating headers from the JSON body):

```
HTTP/1.1 200 OK
Content-Type: application/json

{"username": "<the_username>", "token": <the_calculated_token>}
```

5. Compile your code using `g++ /home/user/auth_api.cpp -o /home/user/auth_api`. Ensure the binary is executable.

To verify your work, I will run the compiled binary with a test input and check the output format and token correctness.