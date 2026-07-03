You are tasked with debugging a failing build system in `/home/user/project`.

When you run `/home/user/project/build.sh`, it fails during the code generation step because the pre-compiled `generator` binary exits with an error. Unfortunately, the source code for `generator` was lost, and the binary has been stripped of debug symbols. It fails silently without providing any useful error messages.

Your objectives are:
1. Use system call tracing to discover what external resources or files `generator` is trying to access and failing.
2. Use binary analysis / reverse engineering tools on `generator` to figure out the exact file contents it expects.
3. Fix the environment by creating the necessary file(s) with the correct content so that `/home/user/project/build.sh` runs successfully and compiles `main`.
4. Once you have successfully built the project, write the exact secret string that `generator` expected into a new file located at `/home/user/secret_found.txt`.

Ensure that you do not modify `build.sh` or `main.cpp`. You must resolve the issue by providing the `generator` binary with the environment and data it requires to succeed.