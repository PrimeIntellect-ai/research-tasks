You are a release manager preparing a deployment for a legacy mathematical computation engine. The system relies on a complex web of shared libraries, but an outdated library is causing calculation errors and needs to be dynamically replaced at the ABI level before deployment. 

The deployment files are located in `/home/user/deploy/`.
Inside this directory, there is a main executable called `math_engine` and several shared libraries (`libcore.so`, `libmath_ops.so`, `liblegacy.so`, etc.). 

Your tasks are to:
1. **Dependency Graph Resolution:** Write a Python script `/home/user/deploy/analyze_deps.py` that parses the ELF dynamic dependencies (e.g., using `ldd` or parsing `readelf`) starting from `math_engine`. It must recursively find all shared libraries within `/home/user/deploy/` that are required. Save the resolved dependency graph as an adjacency list in a JSON file at `/home/user/deploy/deps.json`. The keys should be the filenames of the binaries (e.g., "math_engine", "libcore.so") and the values should be a list of the required local shared library filenames it directly depends on.
2. **Assembly & ABI Replacement:** Through your analysis, you will find that one of the libraries (which depends on `liblegacy.so`) calls a symbol named `calculate_magic_constant`. `liblegacy.so` currently returns an incorrect mathematical constant (0). 
   - Write a minimal x86_64 assembly file `/home/user/deploy/magic.s` (using GNU assembler or NASM syntax) that implements `calculate_magic_constant` to return the integer `42` (the correct mathematical constant).
   - Compile this assembly file into a new shared library named `/home/user/deploy/libmagic.so`.
3. **Linkage Patching:** Use an ELF patching tool (like `patchelf`) to modify the specific intermediate shared library in `/home/user/deploy/` that originally depended on `liblegacy.so`. Change its dependency so it requires `libmagic.so` instead of `liblegacy.so`. Do not break other dependencies.
4. **Execution:** Create a shell script `/home/user/deploy/run_deployment.sh` that sets the appropriate `LD_LIBRARY_PATH` to the current directory and executes `./math_engine`, piping the standard output to `/home/user/deploy/result.txt`. Run this script.

Requirements:
- Ensure the python script strictly outputs the JSON graph of local libraries only (exclude system libraries like `libc.so.6`, `linux-vdso.so`, etc.).
- Ensure your assembly implementation properly adheres to the x86_64 System V ABI.
- Install any necessary build tools or ELF manipulation utilities via `sudo apt-get` (assume passwordless sudo is configured if necessary, though you operate as a standard user).