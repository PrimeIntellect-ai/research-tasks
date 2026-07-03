You are porting an legacy Web Application Firewall (WAF) rule evaluator to run as a microservice in a minimal Linux container environment. Previously, this tool ran as an Apache module, but we are decoupling it into a standalone REST API written in C++. 

You have the following objectives:

1. **Extract the WAF Ruleset (Image Processing)**:
   The master WAF rule for our new minimal environment is documented inside a scanned architecture diagram located at `/app/waf_schematic.png`. You must use `tesseract` (which is pre-installed) to read the text from this image. Somewhere in the extracted text, there is a strict WAF filtering rule formatted as a custom DSL. Extract this exact DSL string.

2. **Implement the WAF Interpreter & REST API (C++)**:
   Create a C++ application at `/home/user/waf_service.cpp`. 
   - You may use the provided single-header HTTP library at `/app/include/httplib.h` and JSON library at `/app/include/json.hpp`.
   - The service must listen on `localhost:8080` and expose a POST endpoint at `/api/v1/evaluate`.
   - The endpoint will receive JSON payloads.
   - You must implement a simple interpreter/evaluator in C++ for the DSL rule extracted in step 1. The DSL syntax is: `DENY IF <json_path> MATCHES <regex_pattern>`.
   - If the JSON payload violates the evaluated rule, return an HTTP 403 status code. If it passes, return HTTP 200.

3. **Orchestrate End-to-End Tests**:
   To ensure your port is successful before deployment, write a test wrapper script at `/home/user/test_waf.sh`. This script should take a single argument (the path to a JSON file), send it to your running C++ REST API via `curl`, and exit with code `0` if the API returns 200 OK, or exit with code `1` if the API returns 403 Forbidden.

Build your C++ service and compile it to `/home/user/waf_service`. Ensure the service is robust enough to not crash on malformed JSON (return 400 Bad Request). Start the service in the background and leave it running, or ensure your wrapper script can start/stop it appropriately.