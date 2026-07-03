You are a developer tasked with organizing and executing a scattered legacy project. 

The project files are located in `/home/user/legacy_project/` and its subdirectories. The project uses a custom, minimal assembly-like language with the extension `.lasm`.

The legacy build system that used to execute these files is lost, and you need to write a Python script `/home/user/run_project.py` that acts as an emulator/interpreter for this language.

**Language Specifications:**
*   **Registers:** There are exactly three global registers: `X`, `Y`, and `Z`. They are all initialized to `0` at the very beginning of the program execution and persist their state across all files.
*   **Instructions** (Tokens are space-separated):
    *   `INC <reg> <val>`: Increases the value of register `<reg>` by the integer `<val>`. (e.g., `INC X 5`)
    *   `DEC <reg> <val>`: Decreases the value of register `<reg>` by the integer `<val>`.
    *   `RUN <filename>`: Resolves a dependency. This instruction pauses execution of the current file, finds `<filename>` anywhere within the `/home/user/legacy_project/` directory tree, and executes it. 
        *   *Crucial Dependency Rule:* If a file has already been fully executed during this run, subsequent `RUN <filename>` calls for that file must be ignored (it should not be executed twice).
    *   `OUT <reg>`: Appends the current integer value of `<reg>` to an output log file.

**Your Objectives:**
1.  Write the Python interpreter `/home/user/run_project.py`.
2.  The interpreter must dynamically scan `/home/user/legacy_project/` to build a map of filenames to their absolute paths, as `RUN` commands only provide the basename (e.g., `RUN init.lasm`). You can assume basenames are unique across the project.
3.  The execution must start with the file `main.lasm` (which is located somewhere in the project tree).
4.  Every time an `OUT <reg>` instruction is encountered, your script should append the value to `/home/user/execution_log.txt` (one value per line).
5.  Run your script to generate the final `/home/user/execution_log.txt`.

Ensure your Python script correctly handles the graph traversal (dependency resolution of `RUN` commands) and the emulator state. Once you write the script, execute it so the log file is generated.