You are a build engineer responsible for creating a lightweight artifact scoring service. To minimize dependencies on the build servers, we need a custom C++ application that evaluates mathematical metrics.

Your task is to implement a standalone C++ REST API server from scratch (using standard POSIX sockets) that parses and evaluates mathematical formulas for artifact scoring.

Requirements:
1. **Fix the Vendored Package:**
   We use the `cxxopts` library for command-line parsing, which is pre-vendored at `/app/vendored/cxxopts`. However, a recent automated refactor accidentally removed a critical standard library inclusion from `/app/vendored/cxxopts/include/cxxopts.hpp`, preventing it from compiling. You must identify the missing standard include (related to string types) and fix the header.

2. **Develop the C++ Server (`/home/user/artifact_scorer.cpp`):**
   * Write a C++ program that uses the fixed `cxxopts` to accept a `--port` argument.
   * Start a TCP socket server listening on the specified port.
   * **State Machine Parser:** Implement an HTTP request parser using a state machine that correctly reads the HTTP headers (until `\r\n\r\n`) and extracts the `Content-Length` to read the request body.
   * The server must accept HTTP POST requests to the endpoint `/score`.
   * The request body will be `application/x-www-form-urlencoded` containing exactly two parameters: `expr` (the mathematical expression) and `x` (a double-precision float value for the variable x). Example body: `expr=3*x^2+2*x-5&x=4.5`.

3. **Numerical Algorithm / Math Parser:**
   * Write a mathematical parser (e.g., recursive descent or Shunting-yard) capable of evaluating the `expr` string.
   * Supported operators: `+` (add), `-` (subtract), `*` (multiply), `/` (divide), `^` (power).
   * It must respect standard mathematical operator precedence and support the variable `x` (substituted with the parsed value).
   * Parentheses `()` for grouping must be supported.

4. **Response Protocol:**
   * Respond with a valid `HTTP/1.1 200 OK` response.
   * Include the `Content-Type: text/plain` and correct `Content-Length` headers.
   * The response body must be solely the evaluated numerical result (rendered as a string, e.g., using `std::to_string`).
   * Handle requests concurrently or sequentially, but the server must stay alive after serving a request.

5. **Build and Run:**
   * Compile your program to `/home/user/artifact_scorer`.
   * Ensure it is running on port `8080` (by passing `--port 8080`) in the background so it can be verified.

Do not use any external libraries other than the standard C++ library and the provided `cxxopts`.