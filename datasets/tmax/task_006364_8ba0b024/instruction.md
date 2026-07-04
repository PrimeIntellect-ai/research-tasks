You are an open-source maintainer reviewing a pull request for a Web Application Firewall (WAF) microservice. 

A contributor submitted a PR located in `/home/user/waf_pr` to add a new gRPC endpoint `EvaluateRisk`, which uses a numerical algorithm to calculate a risk score and a constraint satisfaction model to decide whether to `ALLOW`, `CHALLENGE`, or `BLOCK` a web request. 

However, the PR is broken:
1. The `Makefile` fails to correctly invoke `protoc` with the gRPC C++ plugin, causing missing header files.
2. `waf_service.cpp` has compilation errors due to incorrect gRPC response types and signature mismatches.
3. The numerical risk algorithm in `waf_service.cpp` contains a logical bug: it calculates the `RequestRate` using integer division (`TotalRequests / TimeWindowSeconds`), which truncates the precision and results in incorrect scores. It must be evaluated as a floating-point value.
4. The constraint satisfaction logic is incomplete. It currently only returns `ALLOW` or `BLOCK`. You need to implement the following rules precisely:
   - `RiskScore = (RequestRate * 1.5) + (FailedLogins * 10.0)`
   - If `RiskScore > 50.0`, the action MUST be `BLOCK`.
   - If `RiskScore <= 50.0` BUT `IpTrustScore < 0.2`, the action MUST be `CHALLENGE`.
   - Otherwise, the action MUST be `ALLOW`.

Your task:
1. Fix the `Makefile` so that running `make` successfully compiles the `waf_server` binary.
2. Fix the bugs and implement the missing logic in `waf_service.cpp`.
3. Compile the application by running `make`.
4. Run the server in the background: `./waf_server &`
5. Run the provided integration script: `bash /home/user/waf_pr/test_integration.sh`. This script will send test payloads to the gRPC service and write the results to `/home/user/waf_pr/results.log`.

The task is considered complete when `/home/user/waf_pr/results.log` contains the correct evaluation for all test cases.