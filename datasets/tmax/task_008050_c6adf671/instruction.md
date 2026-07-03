You are a platform engineer maintaining a CI/CD pipeline for a C++ service. The developers have submitted a PR that passes on their local machines (due to stale build artifacts) but is consistently failing on the clean CI runners.

The project is located in `/home/user/ci_pipeline/`. It builds a multi-threaded expression evaluator that is used in our API gateway's dynamic rate-limiting module. 

Currently, the CI pipeline fails in two ways:
1. **Build Failure:** The `Makefile` is misconfigured. When `make` runs in a clean environment, it fails during the linking stage with "undefined reference" errors because it doesn't correctly link all necessary object files into the final executable.
2. **Test Failure:** Once you fix the build step, running `./evaluator test` will fail. The developers added a new subtraction feature to the expression parser, but there is a bug in how subtraction is evaluated (it computes things in the wrong order). Additionally, the tests are run concurrently, so the bug manifests sporadically if not fixed properly.

Your tasks:
1. Fix the `Makefile` in `/home/user/ci_pipeline/` so that running `make` successfully builds the `evaluator` binary from a clean state.
2. Fix the subtraction bug in `/home/user/ci_pipeline/expr_parser.cpp`.
3. After fixing both, run `make clean && make` to rebuild the binary.
4. Run the test suite by executing `./evaluator test` and save the exact standard output of this command to `/home/user/ci_pipeline/test_results.log`. 

The final `test_results.log` must contain the string `ALL TESTS PASSED` to indicate that the evaluator is correctly evaluating the mathematical expressions under concurrency.