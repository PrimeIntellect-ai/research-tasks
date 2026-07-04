We are migrating an old proprietary Web Application Firewall (WAF) analyzer from a legacy Python 2 C-extension to a modern Python 3 gRPC microservice. The core logic must remain in C for performance, but it will be exposed via gRPC. 

Unfortunately, the original `setup.py` is broken, and we lost the source code for the exact risk scoring algorithm. We only have a compiled stripped binary of the legacy tool at `/app/legacy_waf_oracle`.

Your tasks:

1. **Recreate the WAF Logic in C**:
   Write the missing C function `int calculate_risk_score(const char* payload);` in a file named `/home/user/waf.c`.
   The algorithm is a state machine that evaluates characters. Through reverse engineering, we know the basics:
   - Initial `state` = 1
   - `score` = 0
   - Iterate over each character `c` in the string (until null terminator):
     - If `c` is a lowercase vowel ('a', 'e', 'i', 'o', 'u'): `state = (state * 2) % 10`
     - If `c` is a digit ('0'-'9'): `state = (state + (c - '0')) % 10`
     - Otherwise: `state = (state + 1) % 10`
     - After updating the state, add `((int)c * state)` to the `score`.
   You can verify your implementation by comparing its output against the `/app/legacy_waf_oracle` binary, which takes a single string argument and prints the score.

2. **Build the Shared Library**:
   Compile `/home/user/waf.c` into a shared library `/home/user/libwaf.so`.

3. **Design the gRPC Interface**:
   Create a Protobuf file at `/home/user/waf.proto` defining:
   - A package named `waf`
   - A `WafRequest` message with a single field `string payload = 1;`
   - A `WafResponse` message with a single field `int32 score = 1;`
   - A `WafService` with an RPC method `AnalyzePayload` that takes a `WafRequest` and returns a `WafResponse`.

4. **Implement the gRPC Server**:
   Write a Python 3 script at `/home/user/server.py` that:
   - Uses `grpcio` and `ctypes` to load `libwaf.so`.
   - Implements the `WafService` using the generated Protobuf code.
   - Listens on `127.0.0.1:50051` (insecure port).
   - Serves requests indefinitely.

5. **Start the Service**:
   Generate the Python gRPC stubs from `waf.proto`.
   Run your `server.py` in the background (e.g., `python3 /home/user/server.py &`) so that the automated verifier can connect to it.

Make sure you leave the service running and listening on `127.0.0.1:50051`.