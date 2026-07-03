You are tasked with setting up a polyglot build system and implementing the frontend of a custom Web Security Expression Evaluator (WSEE). 

A previous engineer started writing a C++ engine for evaluating Web Application Firewall (WAF) rules at high speed, along with a Python orchestrator, but left the project incomplete. The CMake build system is currently broken (it fails at link time and lacks proper conditional build support), and the Python expression parser is missing.

Your objectives:

1. **Fix the Build System**: 
   The project is located at `/home/user/wsee`. There is a `CMakeLists.txt` file that attempts to build two things: a static helper library `libast.a` and a shared library `libwsee.so`. However, `libwsee.so` fails to link properly against `libast.a`, and it fails to load in Python due to missing position-independent code flags. Fix `/home/user/wsee/CMakeLists.txt` so it successfully compiles.
   Additionally, modify `CMakeLists.txt` to accept a conditional build flag `-DENABLE_STRICT_MODE=ON`. When this flag is passed, it should add the `-DSTRICT_SECURITY` macro definition to the compilation of `libwsee.so`.

2. **Implement Expression Parsing and Custom Data Structures**:
   Write a Python script `/home/user/wsee/compiler.py`. It should contain a function `compile_rule(expression: str) -> str` that parses a simple WAF DSL and returns a JSON string representing the AST. 
   * Supported variables: `req.ip_version`, `req.payload_size`, `req.contains_sql`
   * Supported operators: `==`, `<`, `>`, `AND`
   * The AST must be a JSON string of nested dictionaries. 
     * A condition like `req.ip_version == 4` should parse into: `{"type": "condition", "left": "req.ip_version", "operator": "==", "right": 4}`
     * An `AND` operation like `A AND B` should parse into: `{"type": "logical", "operator": "AND", "left": <AST of A>, "right": <AST of B>}`
     * Note: `AND` is strictly binary and left-associative.

3. **Orchestrate and Evaluate**:
   Write a Python script `/home/user/wsee/orchestrator.py` that:
   * Uses the `subprocess` module to compile the C++ project using CMake, ensuring the `-DENABLE_STRICT_MODE=ON` flag is passed. The build directory should be `/home/user/wsee/build`.
   * Uses `ctypes` to load `/home/user/wsee/build/libwsee.so`.
   * Maps the following C struct using `ctypes`:
     ```c
     struct WebRequest {
         int ip_version;
         int payload_size;
         int contains_sql;
     };
     ```
   * The C++ library exposes: `extern "C" int evaluate_ast(const char* ast_json, struct WebRequest* req);`
   * Create a `WebRequest` with `ip_version=4`, `payload_size=800`, `contains_sql=0`.
   * Use `compiler.py` to parse the following rule: `req.ip_version == 4 AND req.payload_size < 1000 AND req.contains_sql == 0`
   * Pass the generated JSON AST and the struct to `evaluate_ast`.
   * Write the integer result returned by `evaluate_ast` to `/home/user/wsee/evaluation_result.txt`.

Ensure `/home/user/wsee/orchestrator.py` creates `/home/user/wsee/evaluation_result.txt` containing only the final integer evaluation result (e.g., `1` for true, `0` for false).