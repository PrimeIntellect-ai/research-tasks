You are a build engineer responsible for an internal artifact versioning tool. Your workspace is located at `/home/user/artifact_manager`. 

Inside this directory, there is a C program (`version_bumper.c`) that takes a semantic version string (like `1.2.3`) and an operation (`patch`, `minor`, or `major`) and outputs the incremented version. However, the build system and tests are currently incomplete or broken.

Your task is to fix the build, implement a custom property-based test in Bash, and orchestrate a mini-CI pipeline.

**Step 1: Fix the Build**
There is a `Makefile` in the directory, but it is broken and fails to compile the `version_bumper` binary. Diagnose and fix the `Makefile` so that running `make` successfully compiles the C program into an executable named `version_bumper`.

**Step 2: Implement Property-Based Testing**
Create a Bash script at `/home/user/artifact_manager/test_property.sh` that performs property-based testing on the `version_bumper` binary. The script must:
1. Generate 50 random semantic versions (format `X.Y.Z`, where X, Y, and Z are random integers between 0 and 99 inclusive).
2. For each generated version, run `./version_bumper <version> patch` to get the new version.
3. Implement pure Bash logic to strictly compare the semantic versions. You must verify the property that the new version is strictly greater than the original version according to semver rules.
4. If the property holds for all 50 versions, the script should print "All tests passed" and exit with status `0`.
5. If any test fails, the script should print an error and exit with status `1`.
6. Ensure the script is executable.

**Step 3: Orchestrate the CI Pipeline**
Create a Bash script at `/home/user/artifact_manager/ci_pipeline.sh` that coordinates the build and test process. The script must:
1. Run `make clean` and `make`. If compilation fails, exit `1`.
2. Run `./test_property.sh`. If the tests fail, exit `1`.
3. If both compilation and testing succeed, calculate the SHA-256 checksum of the compiled `version_bumper` binary (just the hash, no filenames).
4. Write the final result to `/home/user/artifact_manager/pipeline_report.txt` exactly in this format:
   `SUCCESS: <sha256_hash>`
5. Ensure the script is executable.

To complete this task, fix the `Makefile`, write the two Bash scripts, and finally run your `./ci_pipeline.sh` to generate the report.