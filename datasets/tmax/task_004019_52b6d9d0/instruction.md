You are an open-source maintainer reviewing a pull request for a polyglot project: a simple custom bytecode interpreter written in Rust, wrapped with a shell-based build and execution orchestrator. 

The PR attempts to add a new character decoding instruction (XOR decryption) to the interpreter, but the CI pipeline is failing due to a Rust borrow checker error.

Your task is to:
1. Inspect the source code at `/home/user/repo/interpreter.rs`.
2. Fix the Rust ownership/borrow checker error preventing compilation. Do not change the logic of the interpreter, just fix the compilation error.
3. Run the build script `/home/user/repo/build.sh` to compile the executable.
4. Execute the wrapper script `/home/user/repo/run.sh /home/user/repo/data.enc` to interpret the encoded payload.
5. Save the standard output of the `run.sh` command exactly to `/home/user/decoded_message.txt`.

The project is located in `/home/user/repo/`. You only need standard Linux tools and the pre-installed Rust toolchain.