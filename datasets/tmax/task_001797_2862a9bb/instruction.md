You are a script developer tasked with fixing a broken C build pipeline.

You have a project located in `/home/user/project` that consists of a C program, a Protobuf message definition (`message.proto`), and a `Makefile`. Currently, the `Makefile` contains a circular dependency that prevents the project from building, and the Protobuf files have not been generated.

Your task is to write a Bash utility script that automates the fixing, building, and execution of this project.

Specifically, you must:
1. Identify the circular dependency in `/home/user/project/Makefile` and create a standard patch file named `/home/user/project/Makefile.patch` that fixes it (the `.o` targets should only depend on their respective `.c` and `.h` files, not on other `.o` files).
2. Create an executable Bash script at `/home/user/project/build_and_run.sh` that performs the following steps in order:
   a. Applies your `Makefile.patch` to fix the `Makefile`.
   b. Uses `protoc-c` to compile `message.proto` into C source and header files (`--c_out=.`).
   c. Runs `make` to compile the `app` executable.
   d. Runs the resulting `./app` executable and redirects its standard output to `/home/user/result.txt`.
3. Execute your script so that the application is built and `/home/user/result.txt` is successfully generated.

Ensure that all file paths are exact and your Bash script handles the steps cleanly.