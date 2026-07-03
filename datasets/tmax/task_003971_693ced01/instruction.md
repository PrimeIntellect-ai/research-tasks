You are an integration developer responsible for testing an API gateway. The team is migrating payload validation logic from a slow Ruby script to a high-performance Bash script before passing requests to our internal API mock server.

Your task consists of four main objectives:

1. **Fix and Build the API Mock Server**
   We vendor a clone of `go-httpbin` to test our API integrations locally. Its source is located at `/app/go-httpbin`.
   However, the repository currently fails to build due to a deliberate perturbation introduced during a bad merge. Find the issue in the Go source or configuration, fix it, and compile the binary to `/app/go-httpbin/httpbin`. You do not need to run the server permanently, but you must ensure the binary successfully compiles and executes its help command (`./httpbin -h`).

2. **Translate and Optimize the Payload Filter**
   We have a legacy Ruby script at `/home/user/legacy_filter.rb` that reads a JSON payload from `stdin`, checks for malicious injection patterns, and computes a custom permission bitmask. 
   Translate this logic into a pure Bash script (with the help of `jq`) at `/home/user/gateway_filter.sh`. 
   *Requirement:* To optimize performance, your Bash script must parse the allowed roles and permissions into a custom in-memory data structure (using Bash associative arrays) rather than repeatedly invoking `jq` or external commands for each rule evaluation. 
   The script must read a JSON string from `stdin`. If the payload is valid and safe, it should print "ACCEPT" to `stdout` and exit with code 0. If it is malicious or invalid, it should print "REJECT" to `stdout` and exit with code 1.

3. **Verify Against the Corpora**
   Your translated script `/home/user/gateway_filter.sh` must correctly classify a suite of test payloads:
   - Valid payloads are stored in `/app/corpora/clean/`
   - Malicious payloads (e.g., mismatched types, invalid bitmasks, XSS attempts) are in `/app/corpora/evil/`
   You must ensure your script rejects 100% of the evil payloads and accepts 100% of the clean payloads. 

4. **Performance Benchmarking**
   Create a benchmarking script at `/home/user/benchmark.sh` that loops 500 times over the file `/app/corpora/clean/payload_01.json`, feeding it to `/home/user/gateway_filter.sh`. 
   The script should use the `time` command (or similar) to measure the total execution time of the 500 iterations and append the real elapsed time (in seconds or milliseconds) to `/home/user/benchmark_results.txt`.

Ensure your final `gateway_filter.sh` is executable and accurately reflects the rules present in the Ruby implementation.