You are the on-call engineer for your company's core platform. It is 3:00 AM, and you have just been paged because the `auth-service` CI pipeline is failing intermittently on the master branch, blocking a critical hotfix deployment. 

The CI reports show two distinct issues:
1. Sometimes the build fails with a Go compiler/linker error.
2. When the build succeeds, the test suite sometimes fails with a crash during concurrent execution.

The source code is located in `/home/user/auth-service`.

Your objectives:
1. Diagnose and fix the environment/configuration issue causing the linker error when building the service. The service does not actually require any external C libraries to compile, but a misconfiguration is forcing it to look for one. Fix the build process or source files so that `go build` runs successfully without relying on external shared libraries not present in the system.
2. Reproduce the intermittent test failure. It is suspected to be a concurrency bug.
3. Fix the underlying issue in the Go code so that `go test -race ./...` reliably passes 100% of the time.
4. Verify your fixes by running the tests.

Once you have fixed both the build and the tests, create a file at `/home/user/resolution.json` with the following exact keys:
- `"build_fix"`: A short string describing the file you modified to fix the linker error (e.g., `"main.go"`, `"Makefile"`, or `"build.sh"`).
- `"bug_type"`: A short string describing the type of concurrency bug you fixed in the Go code (e.g., `"deadlock"`, `"race condition"`, `"resource leak"`).
- `"fixed_variable"`: The exact name of the Go variable that was the root cause of the intermittent test crash.

Ensure your code changes are saved and the service can be built and tested via standard `go` commands in `/home/user/auth-service`.