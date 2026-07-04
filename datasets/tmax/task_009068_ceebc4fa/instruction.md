You are acting as a Release Manager preparing a new polyglot algorithmic microservice for deployment. The service consists of highly optimized C and Go binaries wrapped by a Python REST API. 

Your task is to orchestrate the build process, implement the Python REST API, and write a mock-based test suite to ensure the build pipeline is robust.

I have placed the source code for the algorithms in the following files:
1. `/home/user/src/fibo.c` - A C program that takes a single integer argument `n` and prints the `n`-th Fibonacci number to stdout.
2. `/home/user/src/prime.go` - A Go program that takes a single integer argument `n` and prints the `n`-th prime number to stdout.

You need to perform the following steps:

1. **Polyglot Build Orchestration**:
   Write a Python script at `/home/user/release/build.py` that compiles both programs. 
   - Compile `fibo.c` using `gcc` and output the binary to `/home/user/release/bin/fibo`.
   - Compile `prime.go` using `go build` and output the binary to `/home/user/release/bin/prime`.
   (You will need to create the `bin` directory).

2. **REST API Construction**:
   Write a Flask application in `/home/user/release/server.py` that exposes two endpoints:
   - `GET /api/fibo/<n>`: Calls the compiled `fibo` binary using Python's `subprocess` module and returns a JSON response: `{"algorithm": "fibonacci", "n": <n>, "result": <binary_output>}`
   - `GET /api/prime/<n>`: Calls the compiled `prime` binary using `subprocess` and returns: `{"algorithm": "prime", "n": <n>, "result": <binary_output>}`
   Convert `<binary_output>` to an integer in the JSON response.

3. **Test Fixture and Mock Setup**:
   Write a pytest test suite at `/home/user/release/test_server.py`. 
   The test suite must use `unittest.mock.patch` as a pytest fixture to **mock `subprocess.run`**. The test must NOT call the actual binaries. 
   Configure the mock such that:
   - When mocked `subprocess.run` is called with the `fibo` binary and `n=10`, its `stdout` property returns `b'55\n'`.
   - When called with the `prime` binary and `n=5`, its `stdout` property returns `b'11\n'`.
   Write two tests in this file: `test_fibo_endpoint` and `test_prime_endpoint`, which use the Flask test client to hit `/api/fibo/10` and `/api/prime/5`, respectively, and assert that the JSON responses contain the mocked results and verify the mock was called correctly.

4. **Execution**:
   - Run your `build.py` script.
   - Run your tests using `pytest /home/user/release/test_server.py -v > /home/user/release/test_results.txt`.

Ensure all files are created exactly at the specified paths. You may install `flask` and `pytest` using pip.