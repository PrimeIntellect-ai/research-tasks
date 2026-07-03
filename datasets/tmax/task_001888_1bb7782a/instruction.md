I need you to help me organize a project containing legacy custom build scripts. We have a directory of custom `.bld` files that define conditional cross-compilation builds for different architectures. Before we migrate them, I need to know exactly what output files each script generates.

The `.bld` scripts are written in a rudimentary, custom Domain Specific Language (DSL). Your task is to write a Python script that parses and emulates the execution of these scripts to determine what files are produced, and then outputs a structured JSON manifest. Finally, write a unit test for your emulator.

**The DSL Specification:**
The language evaluates sequentially and has no loops. Variables are strings.
*   `TARGET <arch>`: Sets the target architecture (e.g., `TARGET arm64`). Always the first line if present.
*   `DEFINE <VAR> <VALUE>`: Defines a variable and assigns it a string value.
*   `EMIT <filename>`: Declares that a file is generated.
*   `IF <VAR> == <VALUE>`: Starts a conditional block. The block executes only if `<VAR>` is defined and equals `<VALUE>`.
*   `ENDIF`: Closes the conditional block.

**Your Tasks:**
1.  **Create the Organizer Script:** Write a Python script at `/home/user/organizer.py`. It must:
    *   Scan `/home/user/legacy_builds/` for all files ending in `.bld`.
    *   Implement an interpreter/emulator that parses the DSL, tracks defined variables, and evaluates `IF` conditions.
    *   Collect the target architecture and the list of all files emitted (`EMIT`) during the emulated execution.
    *   Output the results to `/home/user/build_manifest.json`.

2.  **Output Format:**
    `/home/user/build_manifest.json` must be a JSON object where keys are the `.bld` filenames (e.g., `app.bld`) and values are objects containing:
    *   `target` (string): The architecture specified by `TARGET` (or `null` if none).
    *   `emitted_files` (list of strings): The filenames produced by `EMIT` commands whose conditions were met.

3.  **Write Tests:** Write a unit test script at `/home/user/test_organizer.py` using the standard `unittest` framework. It must test the parsing and evaluation logic of your DSL interpreter on at least one mock script string that includes an `IF` block.

The legacy build scripts are already located in `/home/user/legacy_builds/`. Please complete the scripts and run your Python script so the `build_manifest.json` is created.