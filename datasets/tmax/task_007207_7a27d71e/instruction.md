You are a Build Engineer managing a polyglot software repository. The project uses a custom dependency resolution system that has been struggling with performance and reliability. 

Your task is to create a new, high-performance build orchestrator in Go that resolves dependency versions, evaluates version expressions, and triggers builds concurrently.

Currently, there is a legacy Node.js script at `/home/user/project/legacy_semver.js` that contains the specific, proprietary logic used to parse our internal version formats and evaluate logical expressions. 

You must write a Go program at `/home/user/project/orchestrator.go` that does the following:

1. **Code Translation & Version Logic:** Translate the core semantic version evaluation logic from `/home/user/project/legacy_semver.js` into Go. Our internal versioning strictly follows `MAJOR.MINOR.PATCH` (e.g., `1.2.3`). You must support the operators `==`, `>=`, and `<=`, as well as the logical AND operator `&&` connecting two conditions.
2. **Expression Parsing:** Read a dependency manifest file located at `/home/user/project/manifest.txt`. Each line contains a package name and a version expression (e.g., `pkgA >= 1.0.0 && pkgA <= 2.5.0` or `pkgB == 3.0.0`).
3. **Concurrency:** Use Go goroutines and channels to inspect the packages concurrently. For each package listed in the manifest, look inside `/home/user/project/packages/<pkg_name>/`. Read the `version.txt` file in that directory to get the package's current version.
4. **Polyglot Build Orchestration:** 
   - If the current version in `version.txt` satisfies the expression in `manifest.txt`, your Go program must execute the package's build script: `/home/user/project/packages/<pkg_name>/build.sh`.
   - Wait for the build script to finish.
5. **Reporting:** Generate a final report at `/home/user/project/build_report.txt`. 
   For each package in the manifest, write exactly one line in the following format (sorted alphabetically by package name):
   - If successful: `SUCCESS: <pkg_name> <actual_version>`
   - If version fails condition: `FAIL: <pkg_name> <actual_version> (unsatisfied)`
   - If package directory or `version.txt` is missing: `FAIL: <pkg_name> (missing)`

Constraints:
- Do not use external Go libraries for semantic versioning (no `go get`). You must implement the logic yourself by translating the provided legacy script.
- The package inspection and build triggering MUST happen concurrently using goroutines.

Once you have written `orchestrator.go`, compile it and run it so that the builds are triggered and `build_report.txt` is produced.