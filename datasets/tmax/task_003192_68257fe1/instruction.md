You are an open-source maintainer reviewing a PR for a lightweight mathematical microservice called `MathRouter`, located in `/home/user/MathRouter`. 

A contributor submitted a PR to add a new "geometric mean" endpoint, but the CI pipeline is currently broken. You need to review and fix the code to make the CI pipeline pass.

The PR introduces the following issues:
1. **URL Routing & Parameter Parsing**: The URL parser in `src/router.cpp` extracts numbers from requests like `GET /api/geom_mean?vals=1.5,2.0,3.5 HTTP/1.1`. However, the contributor introduced a bug where the parser truncates decimal numbers (treating them as integers) or fails to parse the comma-separated list correctly.
2. **Ownership & Memory Management**: To mimic Rust's strict ownership in C++, our CI pipeline runs a custom use-after-move static analysis. The contributor incorrectly used `std::move()` in the mathematical calculation logic in `src/router.cpp`, causing an ownership violation (use-after-move) when computing the geometric mean.
3. **Test Fixture Setup**: The test fixture in `tests/test_router.cpp` mocks the incoming HTTP requests but expects the wrong JSON key in the response, and the mock server setup is missing its initialization step.

Your task is to:
1. Fix the URL parsing bug in `src/router.cpp` so it correctly extracts `double` values.
2. Fix the use-after-move ownership bug in the geometric mean calculation in `src/router.cpp`.
3. Update the test fixture in `tests/test_router.cpp` so that it correctly initializes the mock and expects the correct response format (the response should be `{"result": <value>}`).
4. Run the CI pipeline script `./ci.sh` from the `/home/user/MathRouter` directory.
5. Save the exact console output of the successful `./ci.sh` run to `/home/user/ci_output.txt`.

The project is fully self-contained in `/home/user/MathRouter`. You only need standard C++ standard library headers. You can build and test your changes at any time by running `./ci.sh`.