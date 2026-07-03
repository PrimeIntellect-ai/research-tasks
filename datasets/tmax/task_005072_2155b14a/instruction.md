You are tasked with fixing and completing a C-based mathematical utility designed for a script developer's toolkit. The project is located in `/home/user/math_project`. 

Currently, the project suffers from a few issues that prevent it from compiling and functioning:
1. **Circular Import:** There is a circular inclusion dependency between `encoder.h` and `decoder.h` that causes compilation to fail. You need to resolve this using proper C forward declarations or by reorganizing the structs, without removing the separate header files.
2. **Build System:** The `Makefile` has a circular dependency in its build targets that causes `make` to loop or fail. Fix the `Makefile` so that `make` successfully builds the executable named `math_router`.
3. **URL Parsing and Routing:** The `main.c` file acts as a simulated API router but the routing logic is incomplete. It receives a simulated URL request as its first command-line argument (e.g., `/api/encode?shift=5&data=Test`). You must implement the parsing logic to extract the `shift` (integer) and `data` (string) parameters. 
4. **Mathematical Encoding:** Implement the encoding logic in `encoder.c`. The requested algorithm is a mathematical shift cipher: for every character in `data`, add the `shift` value to its ASCII decimal value (modulo 256). Then, encode the resulting byte array into an uppercase Hexadecimal string.

**Requirements:**
- The compiled executable must be located at `/home/user/math_project/math_router`.
- If the route is not exactly `/api/encode`, the program should print `404 Not Found` to stdout and exit with code 1.
- If the route matches, it should parse the `shift` and `data` query parameters (you can assume they always appear in that order: `?shift=X&data=Y`).
- Apply the modulo-256 addition to each character in `data`.
- Print ONLY the resulting uppercase Hexadecimal string to stdout and exit with code 0.
- Ensure the project builds cleanly by just running `make` in `/home/user/math_project`.

Once you have fixed the code and built the binary, run it with the following argument and save its stdout to `/home/user/math_project/run.log`:
`/api/encode?shift=14&data=AgentTraining`

Do not use external libraries other than the standard C library (`libc`). Ensure your Makefile compiles the C files into object files and links them correctly.