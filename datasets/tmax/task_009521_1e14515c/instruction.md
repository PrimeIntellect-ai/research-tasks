You are a web developer working on a custom API Gateway router for a new microservices architecture. The router is written in Go and is located in `/home/user/gateway`.

The router supports parameterized URL routing with constraint satisfaction. For example, registering the route `/users/{id:int}` should strictly match `/users/123` but NOT `/users/123a` or `/users/abc`. 

However, there is a bug in the routing logic. The parameter parsing and constraint satisfaction fail to strictly enforce the bounds of the route parameters. 

Your task is to:
1. Examine the router implementation in `/home/user/gateway/router.go`.
2. Fix the bug in the regex compilation logic so that routes only match if the constraints are strictly satisfied for the entire path segments (no partial matches within a segment or overflowing bounds).
3. Create a property-based test in `/home/user/gateway/router_prop_test.go` using the standard `testing/quick` package. The test should generate random string paths and verify that paths containing non-numeric characters in the `id` segment do NOT match the `/users/{id:int}` route.
4. After fixing `router.go`, generate a unified diff patch of your changes against the original `router.go` and save it to `/home/user/gateway/fix.patch`.
5. Run your tests and save the output of `go test -v ./...` to `/home/user/gateway/test_results.log`.

The system must end up with a passing test suite, a valid patch file, and a correctly functioning router.