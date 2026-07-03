You are a web developer working on a backend request filtering component in C++. The component validates incoming request payloads and applies a rate limit per user. 

You have been given a partial project in `/home/user/rate_limiter` containing:
- `main.cpp`: The entry point that reads requests and calls the rate limiter and validator.
- `rate_limiter.h` / `rate_limiter.cpp`: A fixed-window rate limiter allowing 3 requests per 10 seconds per user. 
- `validator.py`: A Python prototype of the payload validation logic.
- `requests.txt`: A file containing a stream of incoming requests (format: `user_id timestamp payload`).

Your task:
1. The `rate_limiter.cpp` file contains a memory safety issue (undefined behavior due to an out-of-bounds array access) that causes crashes. Find and fix the bug so it correctly enforces the limit of 3 requests per 10 time units.
2. Translate the Python validation logic in `validator.py` into C++. Create a new file `validator.cpp` that implements the function `bool validate_request(const std::string& payload);` (as expected by `main.cpp`).
3. Compile `main.cpp`, `rate_limiter.cpp`, and `validator.cpp` into an executable named `server_bin` in the `/home/user/rate_limiter` directory. You may use `g++` with standard C++17.
4. Run your executable with the provided inputs: 
   `./server_bin /home/user/rate_limiter/requests.txt /home/user/rate_limiter/results.txt`

Ensure that the final output file `/home/user/rate_limiter/results.txt` is created and correctly populated with "ACCEPTED", "LIMITED", or "INVALID" for each request.