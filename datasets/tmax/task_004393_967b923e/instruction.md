You are a web security developer working on a C++ WebSocket proxy. The proxy filters incoming connection upgrades based on the client's semantic version and a security policy expression.

You have a small C++ project located at `/home/user/ws_filter`. However, the build is currently broken due to a Makefile linking error, and the expression parsing logic is incomplete.

Your tasks are:
1. Fix the build issue in `/home/user/ws_filter/Makefile` so that running `make` successfully produces the `ws_filter` binary. Do not change the compiler from `g++`.
2. Implement the missing logic in `/home/user/ws_filter/policy.cpp` for the `bool evaluate_policy(const std::string& client_version, const std::string& expression)` function. 
   - The `expression` will always be in the format: `V [operator] [semver]`, where `[operator]` can be `<`, `>`, `<=`, `>=`, or `==`. Example: `V >= 1.2.0`.
   - You must parse the operator and target version from the string and use the provided `compare_semver` function (declared in `semver.h`) to evaluate if the client's version satisfies the policy.
3. Once compiled, run `./ws_filter ws_requests.txt > /home/user/allowed.log`.

The `/home/user/ws_filter/ws_requests.txt` file contains one connection attempt per line in the format:
`[ConnectionID] | [ClientVersion] | [PolicyExpression]`

The resulting `/home/user/allowed.log` must contain exactly the `ConnectionID` of each connection that satisfies its policy expression, with one ID per line.