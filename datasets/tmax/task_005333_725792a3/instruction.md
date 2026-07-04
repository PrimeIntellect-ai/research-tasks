We are migrating our microservices to minimal Alpine Linux containers, but we've hit a roadblock. One of our legacy tools, a dynamically linked Rust binary located at `/app/legacy_router`, is failing in the new environment due to missing glibc dependencies. 

Your task is to reverse-engineer the behavior of this stripped binary and write a pure Python 3 drop-in replacement at `/home/user/router_port.py`. 

The binary takes a single command-line argument containing a URL string, parses its routing and parameters, normalizes character encodings, and outputs a canonicalized string representation to standard output. If the input is fundamentally malformed, it outputs an error.

Here is what you need to do:
1. **Analyze the Binary:** Experiment with `/app/legacy_router` by passing it various URLs. Pay close attention to how it handles:
   - Percent-encoded characters in paths and queries (e.g., `%20`, `%E2%98%83`).
   - Path traversal normalization (e.g., `/api/v1/../v2/`).
   - Query parameter sorting and parsing.
   - Malformed URLs.

2. **Implement the Port:** Create `/home/user/router_port.py` such that `python3 /home/user/router_port.py "<url>"` produces the exact same standard output and exit code as `/app/legacy_router "<url>"` for any given input.

3. **Property-Based Testing:** To ensure your port is robust and bit-exact equivalent, write a property-based test suite using the `hypothesis` library in `/home/user/test_router.py`. This test should generate random URLs (both valid and edge cases) and assert that the output of your Python script matches the output of the legacy binary.

4. **CI/CD Integration:** We need this tested in our pipeline. Create a bash script at `/home/user/ci_test.sh` that sets up a virtual environment, installs necessary dependencies (like `pytest` and `hypothesis`), and runs your test suite. Ensure this script is executable.

Constraints:
- Your final Python implementation must only use the Python standard library.
- Do not attempt to use `ctypes` or `subprocess` to call the binary in `router_port.py`. It must be a pure Python implementation.

The final verification will involve fuzzing your `router_port.py` against `/app/legacy_router` with thousands of random, adversarial URL strings.