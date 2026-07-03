You are a developer stepping in to fix a broken mathematical C project. The build script `/home/user/math_build/build.sh` is currently failing to compile the project.

There are three main issues you need to resolve:
1. **Dependency Conflict:** The build script is trying to pull in headers from a deprecated dependency version, causing compiler errors. You need to adjust the include paths in the Bash script to use the correct version (`v1` instead of `v2`).
2. **Linker Error:** Even when the compiler errors are fixed, the build will fail during the linking stage because it uses standard C math functions but fails to link the math library. You must update the `build.sh` script to fix this.
3. **Missing Secret:** The compiled executable requires an environment variable `MATH_API_KEY` to run. A previous developer hardcoded this key into the build script for testing, but later removed it for security reasons. You need to perform Git forensics on the `/home/user/math_build` repository to recover this secret key.

Your task:
1. Fix `/home/user/math_build/build.sh` so that it successfully compiles `matrix_magic.c` into an executable named `matrix_magic`.
2. Recover the `MATH_API_KEY` from the git history.
3. Execute the compiled `./matrix_magic` program with the recovered `MATH_API_KEY` set as an environment variable.
4. The program will output a single floating-point number. Save this exact output to a file located at `/home/user/result.txt`.