You are a QA engineer responsible for testing and modernizing our data processing pipeline. 

We currently have a legacy expression evaluator compiled as a stripped executable located at `/app/legacy_evaluator`. It reads JSON from standard input, evaluates mathematical expressions over provided variables, and writes JSON to standard output. 
Example usage:
`echo '{"expr": "(A + B) * C", "data": {"A": 5, "B": 3, "C": 2}}' | /app/legacy_evaluator`
Output:
`{"result": 16}`

This binary is slow because it has to be invoked as a separate process for every evaluation. We want to replace it with a modern, high-throughput gRPC microservice written in Python.

Your task is to:
1. Define a Protocol Buffers schema at `/home/user/evaluator.proto` with the following specification:
   - A `EvalRequest` message containing a string `expr` and a map of strings to integers `data`.
   - A `EvalResponse` message containing an integer `result`.
   - A service `Evaluator` with an RPC method `Evaluate` that takes `EvalRequest` and returns `EvalResponse`.
2. Compile the protobuf file for Python using `grpcio-tools`.
3. Reverse-engineer the behavior of `/app/legacy_evaluator` (it supports basic arithmetic operators: `+`, `-`, `*`, and parentheses) and write a Python gRPC server at `/home/user/server.py` that implements this exact logic. It must listen on `[::]:50051`.
4. Write a property-based test script at `/home/user/test_pbt.py` using the `hypothesis` library. This script should generate random valid expressions and variable sets, send them to both the legacy binary (via `subprocess`) and your new gRPC service, and assert that the outputs match identically.
5. Leave your gRPC server running in the background on port 50051.

Your new Python implementation must correctly parse and evaluate the expressions exactly as the stripped binary does, respecting operator precedence.