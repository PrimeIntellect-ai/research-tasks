You are an engineer tasked with porting a legacy Linux telemetry processor to run inside a minimal container environment. 

You have been given a legacy C tool located in `/home/user/legacy_tool/`. It is meant to parse a data file and output statistics. However, because it was written for a specific old server, it has several issues preventing it from compiling and running in our current environment. 

Your objectives are:

1. **Fix the Makefile and C Source Code:**
   - The `Makefile` in `/home/user/legacy_tool/` is currently broken and fails to run (the original author used spaces instead of tabs for the `build` target, and specified an incorrect compiler flag). Fix the Makefile so that simply running `make` inside the directory successfully builds the `fast-stat` binary.
   - The C source file `fast-stat.c` has a compilation error (missing standard library headers). Fix it.
   - The C source file currently hardcodes the input file path to `/var/log/legacy_telemetry.log`. In our minimal container, this file doesn't exist. Modify the C code to read the file path from the `DATA_FILE` environment variable instead. If the environment variable is not set, it should exit with code 1.

2. **Develop a Rust Wrapper:**
   - Initialize a new Rust project named `telemetry_parser` inside `/home/user/wrapper/`.
   - Write a Rust program that programmatically executes the compiled `/home/user/legacy_tool/fast-stat` binary.
   - The Rust program must set the `DATA_FILE` environment variable to `/home/user/data/input.txt` for the child process.
   - The legacy C tool outputs data in a quirky custom format like this:
     ```
     --- STAT REPORT ---
     Records: <number>
     Anomalies: <number>
     Duration: <number>
     --- END ---
     ```
   - Your Rust wrapper must parse the standard output of the C tool and transform it into strict JSON. 
   - The wrapper must write this JSON to `/home/user/report.json` with the following schema:
     ```json
     {
       "records": <number>,
       "anomalies": <number>,
       "duration": <number>
     }
     ```
   - Make sure your Rust project properly manages its dependencies (e.g., using `serde` and `serde_json`).

3. **Execution:**
   - Build your Rust project.
   - Run the compiled Rust binary to generate the final `/home/user/report.json` file.

Do not ask for root permissions. All operations should be performed as the current user.