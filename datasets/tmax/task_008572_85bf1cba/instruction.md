I have a small C project located in `/home/user/project/` that is managed by a Bash build script named `build.sh`. 

When I run `./build.sh`, the build fails with a linker error (something about an "undefined reference"). I need you to act as a developer debugging this failing build. 

Your tasks are:
1. Diagnose the issue by analyzing the compiler/linker errors and tracing the intermediate state of the build script.
2. Fix `/home/user/project/build.sh` so that it correctly builds the project and produces an executable named `app`.
3. Construct a regression test script at `/home/user/project/test_build.sh` written in Bash. This script should:
   - Run `./build.sh`
   - Verify that the executable `app` exists and is executable
   - Return an exit code of `0` if the build and verification succeed, or `1` if they fail.
   - Make sure `test_build.sh` itself is executable.

Please fix the build and create the required test script.