You are an engineer tasked with setting up a custom, minimal polyglot build system and end-to-end test orchestrator using Bash. 

You have a C++ project in `/home/user/project` that consists of:
1. A protobuf definition for a math service (`math_service.proto`).
2. A numerical algorithm implemented in a separate file that calculates the sum of an arithmetic progression (`algo.h` and `algo.cc`).
3. A main application (`main.cc`) that parses a custom URL scheme (e.g., `math://service/compute?limit=X`), extracts the parameter, calls the numerical algorithm, and populates the protobuf message.

The project currently has no build system. Your task is to write a bash script at `/home/user/project/build_and_run.sh` that acts as the build orchestrator and end-to-end test runner. 

The bash script must do the following in order:
1. Generate the C++ protobuf bindings from `math_service.proto`.
2. Compile `algo.cc` into a shared library named `libalgo.so`.
3. Compile `main.cc` and the generated protobuf C++ source into an executable named `math_runner`.
4. Link `math_runner` against `libalgo.so` and the standard protobuf libraries. **Crucially**, you must ensure that `math_runner` can find `libalgo.so` at runtime without requiring the user to manually export environment variables before running it (e.g., using rpath).
5. Execute `math_runner`, passing the URL routing string `"math://service/compute?limit=15"` as the first and only argument.
6. Redirect the standard output of the executable to `/home/user/project/output.log`.

Make sure your bash script has executable permissions and works when run simply as `./build_and_run.sh` from within the `/home/user/project` directory. The standard Ubuntu packages `g++`, `protobuf-compiler`, and `libprotobuf-dev` are already installed on the system.

After writing the script, execute it to generate the binary and the `output.log` file.