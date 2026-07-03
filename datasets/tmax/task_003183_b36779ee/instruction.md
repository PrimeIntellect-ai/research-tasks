We are migrating our legacy Python 2 voice-calculator backend to a modern stack. The legacy system used Python 2 `eval()` directly on voice transcripts, which was slow, insecure, and incompatible with our move to Python 3. 

Your task is to build a new Rust-based microservice to handle the expression parsing and evaluation. To ensure backward compatibility with some legacy C++ systems during the transition, the core logic must be compiled as a C-ABI shared library, which the Rust gRPC server will then wrap.

Here are your instructions:

1. **Audio Processing:**
   You will find an audio file at `/app/legacy_equation.wav`. This contains a spoken mathematical expression (in English words, e.g., "two plus three times four"). 
   Transcribe this audio. You may use any available tools (like Whisper or standard Python speech recognition libraries).
   Write the transcribed text to `/home/user/transcript.txt`.

2. **Core Evaluator (Shared Library):**
   Create a Rust crate named `math_core` in `/home/user/math_core` configured as a `cdylib`.
   It must implement a robust mathematical expression parser that supports basic arithmetic operations (+, -, *, /) and parentheses.
   Expose a C-ABI compatible function with the following signature:
   `double evaluate_expr(const char* expr);`
   The function should parse the string representation of the math, evaluate it, and return the `double` result. It must gracefully handle invalid inputs by returning `NaN`. 

3. **gRPC Service:**
   Create a second Rust crate named `calculator_grpc` in `/home/user/calculator_grpc`. 
   Define a Protocol Buffer file `calculator.proto` with:
   - Package: `calculator`
   - Service: `Calculator`
   - RPC: `rpc Evaluate (EvaluateRequest) returns (EvaluateResponse);`
   - `EvaluateRequest`: contains a single string field `expression` (tag 1).
   - `EvaluateResponse`: contains a single double field `result` (tag 1).

   Implement this gRPC service using the `tonic` framework. 
   The service must dynamically link to or wrap the `libmath_core.so` shared library you built in step 2 to evaluate the expression.
   The service must listen on `127.0.0.1:50051`.
   **Authentication:** The gRPC service must intercept requests and ensure the metadata contains an `authorization` header with the exact Bearer token: `Bearer MIGRATE_PY3_TOKEN`. Reject unauthorized requests.

4. **Integration/Log:**
   Start the gRPC service in the background.
   Using the transcript you obtained in Step 1, formulate the equivalent mathematical string (e.g., "2 + 3 * 4"), call your running gRPC service using a tool like `grpcurl` or a short Python 3 script, and write the final calculated numeric result to `/home/user/audio_result.txt`.