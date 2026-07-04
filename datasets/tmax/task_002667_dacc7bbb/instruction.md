You are a QA engineer tasked with setting up a test environment to validate a new telemetry processing pipeline. To do this, you need to create a C++ test tool that parses serialized binary test data, processes it through a state machine, performs a statistical calculation, and serializes the result.

Your task is to implement this tool from scratch in C++.

**Requirements:**

1. **Input Data Parsing (Deserialization):**
   Read a binary file located at `/home/user/test_data.bin`. 
   The file consists of a sequence of 9-byte records. Each record contains:
   - A 1-byte unsigned integer representing a Command.
   - An 8-byte double-precision floating-point number (IEEE 754, little-endian) representing a Value.

2. **State Machine Processing:**
   Process the records sequentially using a state machine with two states: `IDLE` and `ACTIVE`. The machine starts in the `IDLE` state.
   - **Command 0x01 (START):** Transitions the state machine to `ACTIVE`. The accompanying Value is ignored.
   - **Command 0x02 (DATA):** If the state is `ACTIVE`, collect the accompanying Value for later calculation. If the state is `IDLE`, ignore the Value.
   - **Command 0x03 (STOP):** Transitions the state machine to `IDLE`. The accompanying Value is ignored.
   - Any other Command should be ignored.

3. **Numerical Algorithm:**
   Once the entire file has been parsed, calculate the population variance of all collected valid Data values. 
   *Population Variance Formula: `sum((x_i - mean)^2) / N`*
   If no valid values were collected, the variance is 0.0.

4. **Output Generation (Serialization):**
   Serialize the result as a JSON file at `/home/user/test_result.json`.
   The JSON must be exactly in this format:
   `{"variance": <value>}`
   Where `<value>` is the calculated variance rounded to exactly 4 decimal places (e.g., `66.6667`).

5. **Build System:**
   Create a `Makefile` at `/home/user/Makefile` that compiles your C++ source code into an executable named `/home/user/test_runner`.
   - The compiler must be `g++`.
   - Use the `-std=c++17` and `-O2` flags.
   - The default `make` target should build the `test_runner` executable.

6. **Execution:**
   After writing the code and Makefile, compile your program by running `make` and then execute `./test_runner` to generate the output file.