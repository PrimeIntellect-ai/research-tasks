You are a systems programmer debugging a build process for a custom web security module. 

In `/home/user/app/`, we have a polyglot application comprising C and x86_64 Assembly. It builds a shared library, `libsec.so`, which validates a custom binary token structure. This library is meant to be loaded by a backend service to accelerate authentication checks.

Currently, the build script `/home/user/app/build.sh` is failing to link the shared library correctly. 

Your tasks are:
1. Debug and fix the `/home/user/app/build.sh` Bash script so it successfully compiles and links `crypto_check.c` and `verify_hash.s` into `libsec.so`. Hint: Check common requirements for compiling shared objects in C.
2. Run your fixed `build.sh` to generate `/home/user/app/libsec.so`.
3. Create a Bash script at `/home/user/app/rest_api.sh` that mimics a REST API CGI endpoint. 
   - It should take exactly one argument (the token string).
   - It must call the provided `/home/user/app/test_lib.py <token>` script, which interacts with the compiled `libsec.so`.
   - Based on the exit status of `test_lib.py` (0 for valid, 1 for invalid), `rest_api.sh` must output exactly this JSON to standard output (no other text):
     `{"endpoint": "/api/validate", "token_valid": true}` if the token is valid.
     `{"endpoint": "/api/validate", "token_valid": false}` if the token is invalid.

Make sure your `rest_api.sh` is executable. You can examine the source files to understand the validation logic.