You are a release manager preparing a deployment for a new microservice. The service is a Go-based REST API that performs mathematical operations, specifically calculating the Greatest Common Divisor (GCD) of two numbers.

Currently, the deployment pipeline is blocked because the project in `/home/user/workspace` fails its property-based tests, and manual QA reported that the API routing is broken and returns invalid results.

Your task is to fix the code and build the release artifact.

Here is what you need to do:
1. Navigate to `/home/user/workspace`.
2. Fix the GCD mathematical logic in `main.go`. The property-based tests in `main_test.go` use the `testing/quick` package and are currently failing because the GCD function sometimes returns negative numbers or calculates incorrect values for negative inputs. The GCD of any two integers should always be non-negative.
3. Fix the URL routing in `main.go`. The API uses Go 1.22's enhanced `net/http` routing pattern. The endpoint should respond to `GET /gcd/{a}/{b}` and use `r.PathValue` to parse the parameters. Currently, the route pattern is incorrectly defined.
4. Ensure `go test` passes.
5. Compile the fixed application and place the executable binary exactly at `/home/user/release/math-api`.

Do not change the property test logic in `main_test.go`. Only modify `main.go`.