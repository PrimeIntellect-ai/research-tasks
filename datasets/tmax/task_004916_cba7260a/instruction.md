You are an integration developer responsible for the security filtering of a C++ WebSocket API. 
We have a custom module that pre-validates incoming WebSocket messages to check their JSON structure (serialization format) and enforces a strict connection-level rate limit. 

Currently, the unit tests in `/home/user/test_validator.cpp` are failing due to bugs in the implementation file `/home/user/validator.cpp`.

Your task is to fix the implementation in `/home/user/validator.cpp` based on the following rules:
1. **Payload Validation**: The `validate_payload` function uses standard `std::regex` to structurally validate incoming serialized JSON. It must ONLY accept payloads matching this exact format: `{"id": <one or more digits>, "data": "<one or more alphabetic characters>"}`. The current implementation has a bug in its regex where it doesn't account for the string quotes around the `data` value.
2. **Rate Limiting**: The `check_rate_limit` function receives timestamps in milliseconds. It must only allow a request (return `true`) if the timestamp is at least `100` milliseconds strictly greater than or equal to the last *accepted* timestamp. The current implementation uses an incorrect threshold of 10ms. 

Files provided:
- `/home/user/validator.h` (Do not modify)
- `/home/user/validator.cpp` (Buggy implementation, modify this)
- `/home/user/test_validator.cpp` (Unit tests, do not modify)

Instructions:
1. Fix the bugs in `/home/user/validator.cpp`.
2. Compile the files into an executable named `test_validator` (using `g++ -std=c++17`).
3. Run the compiled tests and redirect the standard output to `/home/user/test_results.log`.

The task is considered successful when the executable runs without assertion failures and writes "ALL TESTS PASSED" to the log file.