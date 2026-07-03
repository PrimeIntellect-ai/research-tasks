You are a security engineer tasked with fixing a custom Bash-based integration testing suite used to test REST and GraphQL API endpoints for a Web Security project. 

The test suite is located at `/home/user/sec_suite`. Currently, the suite is completely broken and fails to run.

Your objective is to fix the test suite by addressing the following three issues:

1. **Circular Sourcing (Import) Issue:**
   Running `/home/user/sec_suite/run_tests.sh` currently crashes due to an infinite recursion loop. The files `auth_tests.sh`, `graphql_tests.sh`, and `rest_tests.sh` circularly source each other. 
   *Fix:* Implement standard Bash include guards (similar to C/C++ `#ifndef` headers) in all the `.sh` files in `/home/user/sec_suite/` so that no file's contents are evaluated more than once per execution.

2. **Semantic Versioning Bug:**
   The test suite dynamically enables certain security tests based on the API version. The function `compare_versions` in `/home/user/sec_suite/utils.sh` is currently performing a naive string comparison, which causes `1.2.10` to incorrectly be evaluated as less than `1.2.9`.
   *Fix:* Rewrite `compare_versions $1 $2` in `/home/user/sec_suite/utils.sh` to correctly parse and numerically compare Semantic Versions (Major.Minor.Patch). It must `echo 1` if `$1 > $2`, `echo -1` if `$1 < $2`, and `echo 0` if `$1 == $2`.

3. **Numerical Algorithm for Fuzzing Payload:**
   The suite requires generating incrementally sized payload strings to test buffer limits, based on the Lucas number sequence.
   *Fix:* Implement the `generate_fuzz_length $1` function in `/home/user/sec_suite/utils.sh` so that it calculates and echoes the N-th Lucas number. The sequence is defined as: $L(0) = 2$, $L(1) = 1$, and $L(n) = L(n-1) + L(n-2)$ for $n > 1$.

Once you have fixed all the issues, run the test suite using:
`/home/user/sec_suite/run_tests.sh > /home/user/test_results.log`

Verify that `/home/user/test_results.log` indicates all tests have passed. You must leave this exact log file on the system as proof of completion.