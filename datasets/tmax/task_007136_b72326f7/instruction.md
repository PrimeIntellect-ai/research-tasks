You are a systems programmer working on a web security auditing tool. The tool consists of a C project located in `/home/user/src/` with the following components:

1. `num.c` / `num.h`: Implements a numerical algorithm (calculates the Shannon entropy of a payload). Requires the math library (`-lm`).
2. `rest.c` / `rest.h`: Constructs a REST API payload. It has a functional dependency on `ws.c` for upgrading connections.
3. `ws.c` / `ws.h`: Implements WebSocket frame construction. It has a functional dependency on `rest.c` for fallback HTTP reporting.
4. `main.c`: The entry point that uses all three modules to generate a security payload.

Currently, the build process is broken. If you try to compile `rest.c` and `ws.c` into separate static libraries (`librest.a` and `libws.a`) and link them, the linker fails due to circular dependencies (undefined references between the two libraries). Furthermore, the numerical module fails to link because of missing math library flags.

Your task is to write a robust Bash build script at `/home/user/build_system.sh` that performs the following steps:
1. Accepts a single argument: either `--debug` or `--release`. 
   - If `--debug` is passed, it should append the `-g -DDEBUG_MODE` flags to all `gcc` commands.
   - If `--release` is passed, it should append the `-O3 -DNDEBUG` flags.
2. Compiles `num.c`, `rest.c`, and `ws.c` into object files (`.o`).
3. Archives them into separate static libraries: `libnum.a`, `librest.a`, and `libws.a`.
4. Compiles `main.c` to `main.o`.
5. Links `main.o` with the static libraries to produce an executable named `/home/user/bin/sec_tool`. 
   *Crucially, you must resolve the circular linking issue between `librest.a` and `libws.a` using GNU linker group flags in your Bash script, and ensure the math library is linked correctly.*

Once the script is written, run it with the `--release` flag to produce the binary.
Then, execute `/home/user/bin/sec_tool` and redirect its standard output to `/home/user/build_output.log`.

Make sure your script creates the `/home/user/bin` directory if it doesn't exist.