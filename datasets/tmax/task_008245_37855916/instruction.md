You are a platform engineer maintaining the CI/CD pipelines. We have a microservice that ingests test log events from various runners. To protect the ingestion API, we need a small C++ mock validator and rate-limiter test harness to process a batch of simulated incoming requests.

Your task is to write a C++ program at `/home/user/process_requests.cpp` that reads a simulated stream of requests from `/home/user/requests.txt`, applies validation and rate limiting, and writes the decoded accepted payloads to `/home/user/accepted_logs.txt`.

The input file `/home/user/requests.txt` (which you will need to read) contains one request per line in the following format:
`<timestamp_integer> <base64_encoded_payload>`

Your C++ program must implement the following pipeline:
1. **Request Validation**: Verify that the `<base64_encoded_payload>` is a valid Base64 string. 
   - A valid Base64 string only contains characters from the standard Base64 alphabet (`A-Z`, `a-z`, `0-9`, `+`, `/`), and optional `=` padding at the end.
   - Its length must be a multiple of 4.
   - If a request contains an invalid Base64 payload, drop it entirely.
2. **Rate Limiting**: Enforce a strict rate limit of **maximum 2 valid requests per second** (based on the `<timestamp_integer>`). 
   - If a valid request arrives but the quota of 2 requests for that specific timestamp has already been consumed by previous *valid* requests, drop it.
3. **Decoding**: For every request that passes both validation and rate limiting, decode the Base64 payload into plain text.
4. **Output**: Write the decoded plain text of each accepted request to `/home/user/accepted_logs.txt`, one per line, in the exact order they were processed.

Compile your program using `g++ -std=c++17 process_requests.cpp -o process_requests` and execute it. 

The file `/home/user/requests.txt` has already been populated with the test fixture data. Ensure your output file is correctly formatted and created at `/home/user/accepted_logs.txt`.