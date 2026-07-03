You are a build engineer managing artifact versioning and deployment rules. We are migrating our internal build-rule evaluator to a gRPC-based microservice architecture, but first, we need to prototype the expression evaluator in Bash and benchmark its performance.

Your task is to complete the following steps:

1. **Create an expression evaluator in Bash:**
   Write an executable script at `/home/user/evaluate.sh`. It should take exactly one argument: a mathematical expression string (e.g., `"MAJOR + MINOR"`). 
   The script must:
   - Source the environment file located at `/home/user/artifact_info.env` (which contains version variables like `MAJOR`, `MINOR`, and `PATCH`).
   - Parse and evaluate the mathematical expression using Bash arithmetic.
   - Print only the integer result to standard output.

2. **Benchmark the evaluator:**
   Write an executable script at `/home/user/benchmark.sh`. This script must:
   - Read a list of expressions from `/home/user/expressions.txt` line by line.
   - For each expression, run `/home/user/evaluate.sh` 100 times to simulate load (you do not need to record the exact time metrics, just perform the loop to stress-test the interpreter).
   - After the 100 iterations for an expression, evaluate it one more time and append the result to `/home/user/evaluation_results.log` in the exact format: `EXPRESSION = RESULT` (e.g., `MAJOR + MINOR = 7`).

3. **Design the gRPC Interface:**
   Create a Protocol Buffers definition file at `/home/user/evaluator.proto` to represent how this service will eventually be exposed.
   - Use `syntax = "proto3";`.
   - Define a service named `ArtifactEvaluator`.
   - Define an RPC method named `Evaluate`.
   - The method should accept an `EvaluationRequest` message containing a single string field named `expression`.
   - The method should return an `EvaluationResponse` message containing a single int32 field named `result`.

Setup instructions:
Assume `/home/user/artifact_info.env` and `/home/user/expressions.txt` already exist. Do not create them. Just write the three files (`evaluate.sh`, `benchmark.sh`, `evaluator.proto`) and execute `/home/user/benchmark.sh` to generate the `/home/user/evaluation_results.log` file.