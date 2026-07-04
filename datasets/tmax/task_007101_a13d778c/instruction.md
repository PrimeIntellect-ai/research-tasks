You are a web developer working on a fast C-based CGI binary for a lightweight web service. The project is located in `/home/user/web-app`.

The program is designed to take a URL query string as a command-line argument, parse the parameters, and serialize them into a JSON object. 

However, the project currently fails to build due to a linking error in the `Makefile`. Your objectives are to fix the build, generate a patch for your fix, and write a simple CI script to verify the application.

Please complete the following steps:
1. Fix the `Makefile` in `/home/user/web-app` so that the project successfully compiles into an executable named `cgi_bin`.
2. The original broken Makefile is backed up as `/home/user/web-app/Makefile.orig`. Create a unified diff patch file named `/home/user/web-app/fix.patch` that captures the changes you made to `Makefile` (i.e., `diff -u Makefile.orig Makefile > fix.patch`).
3. Write a bash script named `/home/user/web-app/ci_test.sh` that simulates a CI/CD pipeline step. The script must:
   - Run `make clean` and `make`.
   - Execute the compiled `./cgi_bin` with the exact argument: `"user=bob&role=admin"`.
   - Capture the output. If the output exactly matches the serialized JSON string `{"user":"bob","role":"admin"}`, the script must exit with status code `0`. If it does not match or if the build fails, it must exit with status code `1`.
   - Make sure `/home/user/web-app/ci_test.sh` is executable.

Do not modify the C source files; only fix the Makefile, create the patch, and write the CI script.