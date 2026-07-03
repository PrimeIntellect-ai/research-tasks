You are acting as a release manager for a Web Application Firewall (WAF) product. You need to prepare the next deployment of the WAF's core parsing module, which is written in C.

The project repository is located at `/home/user/waf_project`.

Your responsibilities for this release are:

1. **Apply a Security Patch**: Apply the patch file located at `/home/user/patch.diff` to the codebase in `/home/user/waf_project`.
2. **Fix Memory Safety Issues**: The newly applied patch introduces a memory leak when a malicious request is blocked. Debug and fix the memory leak in `src/parser.c`. Ensure that all dynamically allocated memory is properly freed before the function returns in all code paths.
3. **Setup a Test Fixture**: Implement a mock request fixture in `tests/mock_request.c`. You must implement the function `void setup_mock_request(HttpRequest *req)` declared in `tests/main.c`. This function should populate the `HttpRequest` struct (defined in `include/waf.h`) with the following statically assigned string literals:
   - `method`: "POST"
   - `uri`: "/login"
   - `header_name`: "X-Malicious"
   - `header_value`: "<script>alert(1)</script>"
4. **Create a CI/CD Script**: Write a bash script at `/home/user/waf_project/ci_pipeline.sh` that automates the build, test, and package phases:
   - It must compile the WAF code with AddressSanitizer enabled to catch memory leaks: 
     `gcc -fsanitize=address -g src/parser.c tests/mock_request.c tests/main.c -o tests/run_tests -I./include`
   - It must execute the resulting binary `tests/run_tests`.
   - If the tests pass and AddressSanitizer detects no memory leaks (exit code 0), the script should create a gzipped tar archive at `/home/user/deployment.tar.gz` containing exactly the `src` and `include` directories (e.g., `tar -czf /home/user/deployment.tar.gz src include`).
   - The script must exit with a non-zero status if the tests fail or if memory leaks are detected. Make sure the script is executable.

Run your script `/home/user/waf_project/ci_pipeline.sh` to produce the final deployment artifact.