You are a QA engineer tasked with setting up and configuring a new end-to-end test environment for an API gateway. The environment consists of a legacy C++ test harness, a newly required Python reverse proxy, and a Python-based payload sanitizer.

You must complete the following four objectives:

1. Fix the Build System Integration
There is a legacy C++ test harness located at `/home/user/legacy_harness/`. This harness uses CMake to build an executable named `tester`. However, the build is currently failing during the linking phase because it cannot find the shared library `libqa_utils.so`. The library is located in a non-standard system directory: `/opt/qa_libs/`. 
Fix the `CMakeLists.txt` file so that `cmake . && make` successfully compiles the `tester` executable without modifying the source code.

2. Code Translation: C++ to Python
The legacy harness contains a file `/home/user/legacy_harness/src/rules.cpp` which defines several string and regex-based rules for detecting malicious payloads.
You must translate this sanitization logic into Python. Create a file `/home/user/sanitizer.py` containing a function with the exact following signature:
`def analyze_payload(filepath: str) -> bool:`
This function should read the contents of the given file path and apply the translated rules. It must return `True` if the payload is safe (clean), and `False` if it violates any of the rules (evil).

3. Adversarial Corpus Refinement
A set of test payloads is provided to validate your translated Python sanitizer. The automated verifier will strictly grade your `sanitizer.py`.
You must ensure your `analyze_payload` function correctly rejects 100% of the malicious payloads and accepts 100% of the safe payloads. (Note: The verifier will use its own hidden corpora, but you can use the principles found in the C++ rules to ensure robustness).

4. Reverse Proxy Configuration
You need to orchestrate a Python reverse proxy to sit in front of our mock backend. Create a script `/home/user/proxy.py` that implements a basic HTTP reverse proxy using standard Python libraries (like `http.server` or `urllib`). 
The proxy must intercept incoming POST requests, save the request body to a temporary file, and pass it to your `analyze_payload` function. If the payload is malicious, return a 403 Forbidden. If safe, forward the request to the upstream backend.
A previous engineer left a photo of the whiteboard with the required network configuration. The image is located at `/app/whiteboard.png`. You must extract the proxy listening port, the upstream backend port, and a required custom authentication header from this image and implement them exactly in your `proxy.py`. The proxy must inject the extracted authentication header into all forwarded requests.

Ensure all Python scripts are executable and gracefully handle standard execution.