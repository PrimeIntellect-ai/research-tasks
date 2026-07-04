You are an engineer setting up a polyglot build system from scratch. As part of this, we need a lightweight, fast request validator and expression parser written entirely in Bash to handle incoming build requests before they hit our gRPC/protobuf backend.

We have an architectural rule-set provided as an image at `/app/rules.png`. You will need to extract the custom request syntax, default values, state machine logic, and exact error codes from this image.

Your task:
1. Analyze the image `/app/rules.png` (you may use `tesseract` or other available tools).
2. Implement a Bash script at `/home/user/parser.sh` that takes exactly one argument (a string representing the incoming build request).
3. The script must parse the expression, evaluate the state, and validate rate limits according to the extracted rules.
4. The script must output a strictly formatted single-line JSON string to standard output, matching the exact keys and structures defined in the image.
5. If an error condition is met, it must output the exact JSON error format specified in the image.
6. Make sure your script is executable (`chmod +x /home/user/parser.sh`).

Your implementation must be perfectly equivalent to our reference binary oracle. We will automatically fuzz your Bash script with thousands of generated inputs to ensure the outputs match bit-for-bit.