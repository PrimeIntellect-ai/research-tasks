You are an open-source maintainer reviewing a pull request (PR) for a lightweight Python web microservice. The PR adds a new routing endpoint for calculating checksums, but the CI pipeline is failing. 

The repository is located at `/home/user/checksum_service`. The broken PR is on the branch `pr-12`.

Your task is to review the branch, fix the bugs so that all unit tests pass, and adhere to the strict memory constraints defined in the test suite.

Specifically, the PR introduces:
1. A custom URL router that parses paths like `/checksum/<algorithm>/<payload>`.
2. Support for two algorithms: `crc32` and `custom_sum`.
3. A unit test suite in `test_service.py` that checks for correctness, proper URL parameter parsing, and memory consumption.

The PR currently has two major bugs:
- **Routing/Parsing Bug:** The URL parameter parsing fails when the payload contains URL-encoded characters (e.g., `%20` for a space). The router needs to properly decode URL parameters before passing them to the checksum functions.
- **Memory/Checksum Bug:** The `custom_sum` algorithm implementation in `checksums.py` calculates the sum of ASCII values of a string repeated 10,000 times. However, the author implemented this by creating a massive string in memory (`payload * 10000`), which violates the memory constraint enforced by `tracemalloc` in the test suite. You need to rewrite `custom_sum` to be mathematically equivalent but use minimal memory (O(1) auxiliary space).

Steps to complete:
1. Navigate to `/home/user/checksum_service` and checkout the `pr-12` branch.
2. Run the tests using `python3 -m unittest test_service.py`. Observe the failures.
3. Fix the URL routing logic in `router.py`.
4. Fix the memory-intensive logic in `checksums.py`.
5. Run the tests again to ensure everything passes.
6. Once the tests pass successfully, run the test suite and redirect the standard error and standard output to `/home/user/test_results.log`. 

The automated test will verify that:
1. `router.py` correctly unquotes URL parameters.
2. `checksums.py` calculates `custom_sum` accurately without blowing up memory limits.
3. The file `/home/user/test_results.log` exists and contains the output of a completely passing test suite (i.e., `OK`).