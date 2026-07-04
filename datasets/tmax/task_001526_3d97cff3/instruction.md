You are tasked with fixing and optimizing a Go data processing utility located at `/home/user/processor`. The utility filters lists of software versions based on semantic versioning constraints.

The project relies on a vendored package, `github.com/Masterminds/semver/v3`, which is pre-downloaded and located at `/app/semver`. However, the vendored package has been tampered with and currently contains a deliberate syntax error that prevents it from compiling. Furthermore, the Go project in `/home/user/processor` is currently trying to fetch the package from the internet instead of using the local vendored copy.

Your tasks are to complete the following:

1. **Fix the Vendored Package**: Locate and fix the syntax error in the vendored package at `/app/semver` so that it compiles successfully.
2. **Configure Dependency**: Update the configuration in `/home/user/processor` so that it uses the local `/app/semver` directory for `github.com/Masterminds/semver/v3` instead of the remote version. No internet connection will be available during the verification step.
3. **Optimize the Code**: The `FilterVersions` function in `/home/user/processor/main.go` is highly inefficient because it compiles the semantic version constraint repeatedly inside a loop. Refactor the function to parse and compile the constraint exactly once, before the loop begins.
4. **Cross-Compilation**: Cross-compile the Go application for two architectures. Save the resulting binaries exactly as:
   - `/home/user/processor/build/processor-amd64` (for `linux/amd64`)
   - `/home/user/processor/build/processor-arm64` (for `linux/arm64`)

The automated verifier will measure the performance of your optimized `FilterVersions` function by running `go test -bench=BenchmarkFilterVersions`. Your optimized function must achieve an execution time of less than 10,000 ns/op on the benchmark.