You are a platform engineer responsible for maintaining our CI/CD pipelines. A recent pipeline run for our multi-language microservices failed because of a circular dependency issue.

You have two main objectives: detect the dependency cycles programmatically and fix the circular import in our Go service.

Phase 1: Cycle Detection (Mathematical / Algorithmic)
There is a file at `/home/user/pipeline/deps.json` containing the dependency graph of all our internal modules. The format is a JSON object where keys are module names and values are lists of module names they depend on.
1. Write a script (in Python, Node, or any standard scripting language available) to parse this JSON and build a custom graph data structure.
2. Implement an algorithm to detect any circular dependencies (directed cycles) in this graph.
3. Output the nodes involved in the shortest detected cycle to `/home/user/pipeline/cycle_report.txt`. The format must be a comma-separated list of the module names in the cycle, in lexicographical (alphabetical) order. For example: `moduleA,moduleB`.

Phase 2: Code Refactoring (Go)
The cycle you detect will point you to a circular import in our Go microservice located at `/home/user/service`.
The `algebra` package and the `geometry` package currently import each other, preventing the code from compiling (`go build ./...` fails).
1. Refactor the Go code in `/home/user/service` to resolve the circular import. You should extract the common data structures (`Point` and `Vector`) into a new package called `types` within the same module, and update the `algebra` and `geometry` packages to use this new `types` package instead. Do not change the underlying mathematical logic of the functions.
2. Write a unit test in `/home/user/service/algebra/algebra_test.go` that tests the `Solve()` function. The test should assert that calling `Solve(Point{X: 1, Y: 2})` returns a `Vector` with `X=1, Y=2`.
3. Ensure that `go build ./...` and `go test ./...` pass successfully in the `/home/user/service` directory.

Phase 3: Integration
Create a bash script at `/home/user/run_ci.sh` that:
1. Runs your cycle detection script.
2. Navigates to `/home/user/service` and runs `go build ./...` and `go test ./...`.
The script should exit with code 0 if all steps succeed. Make sure it is executable.