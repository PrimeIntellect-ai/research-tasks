You are acting as a penetration tester investigating a vulnerability in a data processing pipeline. The system uses JSON Web Tokens (JWT) to authenticate requests and pass Content Security Policy (CSP) configurations to edge nodes.

Your investigation has revealed two major issues:
1. A vendored version of `pyjwt` (located at `/app/pyjwt`) has been deliberately tampered with. It contains a backdoor that incorrectly accepts tokens with the `alg="none"` header, bypassing signature verification entirely.
2. The system is vulnerable to malicious CSP directives being injected through token claims.

Your task is to fix the library and build a token classifier to identify malicious tokens.

**Step 1: Fix the Vendored Package**
Inspect the source code of the `pyjwt` package vendored at `/app/pyjwt`. Locate the deliberate perturbation that allows the `none` algorithm bypass in signature verification, and fix it. Ensure the package correctly rejects unsigned tokens or tokens using the `none` algorithm when a specific algorithm (like `HS256`) is required.

**Step 2: Build the Token Classifier**
Create a Python script at `/home/user/jwt_scanner.py`. This script must act as a classifier for an automated security pipeline.
It must accept a single JWT string via the `--token` argument.

The script must:
1. Ensure it uses the fixed `/app/pyjwt` library (e.g., by manipulating `sys.path` or installing it).
2. Attempt to decode and verify the token using the secret key `vulnerability-scan-2024` and requiring the `HS256` algorithm.
3. If the token is successfully decoded, extract the `csp_directive` claim.
4. Extract the `b64_payload` claim and base64-decode it.
5. The token must be classified as **EVIL** (exit code 1) if ANY of the following are true:
   - The token signature is invalid, missing, or uses a bypassed algorithm (e.g. `none`).
   - The token has expired or is otherwise malformed.
   - The `csp_directive` claim contains the strings `'unsafe-inline'` or `'unsafe-eval'`.
   - The decoded `b64_payload` contains the substring `<script>`.
6. If the token passes all validation and security checks, it must be classified as **CLEAN** (exit code 0).

Your script will be tested against two sets of tokens. Ensure it strictly exits with `0` for clean tokens and `1` for evil tokens, outputting nothing else required. Do not use external libraries other than the standard library and the fixed `/app/pyjwt` package.