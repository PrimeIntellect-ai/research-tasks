You are acting as a release manager preparing a critical deployment of our internal "MathEval" microservice. The security and development teams have provided a final hotfix and the deployment authorization token encoded inside a secure video transmission. 

Your task is to decode the transmission, apply the hotfix, compile the service, and deploy the API.

**Step 1: Decode the Deployment Signal**
There is a video artefact located at `/app/deployment_signal.mp4`. The video is encoded at exactly 1 frame per second. 
Each frame is either completely black or completely white.
- Black frame = bit `0`
- White frame = bit `1`
Every sequence of 8 frames represents a single ASCII character (Most Significant Bit first).
Decode the entire video into an ASCII string.

**Step 2: Apply the Hotfix**
The decoded ASCII string contains two things:
1. A Unified Diff patch for the microservice codebase.
2. A trailing line in the format: `AUTH_EXPR=<mathematical_expression>`

The codebase is located at `/home/user/evaluator/` and contains `main.cpp`, `parser.cpp`, and `parser.h`.
Save the extracted patch and apply it to `/home/user/evaluator/parser.cpp`.

**Step 3: Build the Service**
The codebase is currently missing a build system. Create a `Makefile` in `/home/user/evaluator/` that compiles `main.cpp` and `parser.cpp` into an executable named `matheval_server`. Ensure you link any necessary standard C++ libraries.

**Step 4: Deploy the API**
Evaluate the `<mathematical_expression>` from the `AUTH_EXPR` line in the decoded message. The integer result of this expression is your deployment token.

Run your compiled `matheval_server`. You may need to modify `main.cpp` if it is incomplete; it must act as a basic HTTP server listening on `127.0.0.1:8080`.
The server must meet these specifications:
- Endpoint: `POST /evaluate`
- Headers: Must strictly require `Authorization: Bearer <deployment_token>` (using the evaluated integer token). If missing or incorrect, return `HTTP/1.1 401 Unauthorized\r\n\r\n`.
- Body: A plain text mathematical expression (e.g., `4+5*2`). You can assume inputs will only contain non-negative integers, `+`, `-`, `*`, `/`, and no spaces for simplicity.
- Success Response: `HTTP/1.1 200 OK\r\n\r\n` followed immediately by the plain integer result of evaluating the expression in the body.

Leave the server running in the background listening on port 8080.