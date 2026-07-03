You are a release manager preparing a deployment pipeline. You need to process a large list of software versions, filter out the ones that are eligible for deployment based on Semantic Versioning (SemVer) rules, and then simulate a concurrent deployment process.

Your task consists of three phases:

**Phase 1: Semantic Version Filter (C++)**
Write a C++ program at `/home/user/semver_filter.cpp` that reads a list of versions and filters them.
1. The program must accept three command-line arguments: `<min_version> <input_file> <output_file>`.
2. It should read the text file specified by `<input_file>`, which contains one version string per line.
3. It must implement a basic Semantic Versioning 2.0.0 parser. The versions in the file will strictly follow the format: `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH-PRERELEASE`.
   - `MAJOR`, `MINOR`, and `PATCH` are non-negative integers.
   - `PRERELEASE` is an alphanumeric string (e.g., `alpha`, `rc1`).
   - Standard SemVer comparison rules apply (e.g., `1.0.0-alpha` < `1.0.0`, `2.1.0` > `2.0.9`). For prerelease tags in this task, you can simply use standard alphabetical string comparison if the major.minor.patch are equal (e.g., `1.0.0-alpha` < `1.0.0-beta`).
4. The program must write all versions from the input file that are **greater than or equal to** `<min_version>` to `<output_file>`, each on a new line.

**Phase 2: Concurrent Deployment Simulator (Go)**
To simulate deploying these valid versions quickly, write a Go program at `/home/user/deploy_workers.go`.
1. The Go program must take two arguments: `<input_file>` (the filtered versions) and `<log_file>`.
2. It must read the versions from `<input_file>`.
3. It must implement a **worker pool** using Go concurrency patterns (goroutines and a channel). Create exactly 3 worker goroutines.
4. The workers should receive versions from the channel and append the exact string `Deployed version: <version>` to `<log_file>` (ensure thread-safe file writing or use a results channel to write sequentially in the main goroutine).

**Phase 3: CI/CD Pipeline Script (Bash)**
Create a shell script at `/home/user/ci_pipeline.sh` that automates this:
1. Compiles the C++ program using `g++` (output binary to `/home/user/semver_filter`).
2. Runs the C++ program with `<min_version>` set to `2.0.0-rc1`, input file `/home/user/versions.txt`, and output file `/home/user/valid_versions.txt`.
3. Runs the Go program using `go run` with input `/home/user/valid_versions.txt` and log file `/home/user/deploy_log.txt`.
4. Exits with code 0 if all steps succeed.

*Assume `/home/user/versions.txt` already exists and contains the raw versions.*
Run your CI/CD script once it is complete to generate the final logs.