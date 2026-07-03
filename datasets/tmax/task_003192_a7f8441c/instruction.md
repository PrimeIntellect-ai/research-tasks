You are acting as a DevSecOps engineer responsible for enforcing policy-as-code for our new microservices architecture. We are migrating our API gateway token validation to a high-performance C++ module, but our internal JWT parsing library is currently failing in CI/CD, and we suspect it has a critical security flaw.

Your task consists of three phases:

Phase 1: Fix the Vendored Library
We have a vendored C++ package located at `/app/vendored/libsec-jwt/`. Currently, it fails to build.
1. Diagnose and fix the build configuration issue in its `Makefile`. 
2. We suspect the library contains a critical vulnerability where it accepts JWTs with `alg=none` (the "none" algorithm vulnerability), bypassing signature verification. Locate this vulnerability in the library's source code and fix it so that it strictly requires the `HS256` algorithm and properly validates the HMAC signature using the provided secret.

Phase 2: Create the Policy Enforcer
Write a C++ program located at `/home/user/policy_enforcer.cpp` that uses the fixed `libsec-jwt` library. 
The program must:
1. Accept a single command-line argument: the JWT secret key.
2. Read HTTP request logs from standard input (stdin). Each line of the input will contain exactly one `Authorization` header value in the format: `Bearer <jwt_token>`.
3. Parse and validate the JWT token using the `libsec-jwt` library.
4. Apply the following policy: 
   - If the token is valid, has not expired (the `exp` claim must be greater than the current Unix timestamp, assume current time is 1700000000 for this test), and the `role` claim is `admin`, the request is approved.
   - Any failure (invalid signature, `alg=none`, missing `role`, expired, or malformed header) means the request is blocked.
5. For each input line, output exactly one line to standard output (stdout): either `PASS` or `BLOCK`.

Phase 3: Build the Enforcer
Compile your program to produce an executable at `/home/user/build/policy_check`. Ensure it statically links or correctly dynamic links the fixed `libsec-jwt` library.

Constraints:
- You must use C++ for the policy enforcer.
- Output strictly `PASS` or `BLOCK` on each line, matching the number of input lines.