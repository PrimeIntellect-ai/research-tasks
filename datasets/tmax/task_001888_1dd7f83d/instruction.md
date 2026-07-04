You are a systems programmer debugging a build issue for a new gRPC service. We have a core numerical algorithm library written in C (`libnumalgo`), and a C++ gRPC wrapper service that exposes this algorithm over the network. 

Currently, the project fails to compile due to a linking issue. Additionally, the service requires a rate-limiting configuration which was unfortunately only provided to us as a screenshot.

Your tasks are to:
1. **Extract Rate Limit**: We received an image at `/app/rate_limit.png` which contains text specifying the rate limit (e.g., "Limit: X"). Extract the integer value of this limit and write ONLY the integer to a new file at `/app/rate_limit.txt`. The gRPC server reads this file on startup. (Hint: you can use `tesseract`).
2. **Fix the Build**: Navigate to `/app/workspace/`. You will find a `Makefile`, `numalgo.c`, `numalgo.h`, `server.cc`, and `matrix.proto`. Running `make` currently results in a linking error where the C++ gRPC server cannot find the symbols defined in the compiled C library. Identify the standard C/C++ interoperability issue in the provided files and fix it. 
3. **Run the Service**: Once compiled successfully, start the server binary. It must bind to `0.0.0.0:50051` and stay running in the background.

**Service Details:**
- The protobuf defines a `MatrixService` with a `CalculateDeterminant` RPC. 
- The server performs request validation and tracks the number of requests. If the number of requests exceeds the integer defined in `/app/rate_limit.txt`, it will respond with a `RESOURCE_EXHAUSTED` gRPC status.
- Ensure the server is actively listening on port `50051` when you are done. Our automated verifier will issue gRPC calls to test the numerical correctness, the linking fix, and the rate limiting functionality.