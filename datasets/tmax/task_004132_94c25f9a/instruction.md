You are an open-source maintainer reviewing a pull request for a new gRPC-based calculator microservice. The PR is meant to securely evaluate mathematical expressions provided by clients, but you've noticed several severe security and reliability issues in the implementation. 

The code is located in `/home/user/project/`.
The PR author provided:
- `proto/calc.proto`: The protocol buffer definition.
- `server.py`: The gRPC server implementation.
- `requirements.txt`: Python dependencies.

Your task is to fix `server.py` in-place so that it securely and robustly handles requests. You must implement the following fixes:

1. **Compilation**: Compile the gRPC protobuf file so the server can run. Generate the files inside `/home/user/project/`.
2. **Rate Limiting**: The current `RateLimiter` is completely broken (it shares state across all clients and doesn't reset windows correctly). Rewrite the `RateLimiter` class to independently track requests per `client_id`. It must allow a maximum of 5 requests per rolling 1-second window per client. If a client exceeds this, abort the gRPC context with `grpc.StatusCode.RESOURCE_EXHAUSTED`.
3. **Deserialization Safety**: The payload `b64_expression` is a Base64-encoded string. The current code assumes valid Base64 and valid UTF-8. If decoding fails for any reason (e.g., malformed base64, invalid encoding), catch the error and abort with `grpc.StatusCode.INVALID_ARGUMENT`.
4. **Input Validation & Injection Prevention**: The current code passes the decoded string directly to Python's `eval()`, which is a massive Remote Code Execution (RCE) vulnerability. 
   - Enforce a strict maximum length of 50 characters on the decoded string.
   - Enforce that the decoded string strictly contains ONLY digits (`0-9`), basic arithmetic operators (`+`, `-`, `*`, `/`), parentheses (`(`, `)`), periods (`.`), and whitespace.
   - If either validation fails, abort with `grpc.StatusCode.INVALID_ARGUMENT`.
5. **Evaluation Safety**: Even with character restrictions, math evaluation can fail (e.g., division by zero, syntax errors). Catch these evaluation exceptions and abort with `grpc.StatusCode.INVALID_ARGUMENT`.

You do not need to modify `proto/calc.proto`. Write your fixes directly into `/home/user/project/server.py`.

To verify your work, start the server and test it. We will evaluate your solution by running a test script against your server on port 50051. Ensure the server runs continuously when executed via `python3 server.py`.