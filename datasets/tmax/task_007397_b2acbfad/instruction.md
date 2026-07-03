You are tasked with setting up a custom, polyglot build system orchestrator from scratch. 

We have a proprietary build configuration format called `.poly` which defines build targets across different languages. You need to write a C++ tool that parses this format and translates it into a standard GNU `Makefile`.

Here are the specifications for the `.poly` format:
- A target block begins with `@target <target_name>`.
- Dependencies are declared via `@deps <expression>`. The expression uses `&` to separate dependencies (e.g., `@deps targetA & targetB`). If there are no dependencies, it is written as `@deps none`.
- The programming language is specified via `@lang <Language>` (e.g., C++, Python, Meta).
- The shell command to execute is specified via `@run <command>`.
- Blocks are separated by empty lines. 
- The parser must be implemented using a state machine that transitions between states based on these `@` directives.

Your tasks:
1. Create the C++ tool at `/home/user/polybuild/polygen.cpp`.
2. The tool must accept two command-line arguments: the input `.poly` file and the output `Makefile` file (e.g., `./polygen build.poly Makefile`).
3. The tool must parse the input file, extract the targets, dependencies (translating the `&` separated dependencies into standard space-separated Makefile dependencies, and omitting `none`), and commands.
4. The tool must translate this into a valid GNU `Makefile` and save it to the specified output file. Each target in the Makefile must be followed by its dependencies, and the command on the next line must be indented with a single TAB character.
5. Compile your C++ program: `g++ -std=c++17 /home/user/polybuild/polygen.cpp -o /home/user/polybuild/polygen`
6. Run your generator: `/home/user/polybuild/polygen /home/user/polybuild/build.poly /home/user/polybuild/Makefile`
7. Run `make all` in `/home/user/polybuild/` to execute the integration test pipeline.

The following files already exist in `/home/user/polybuild/`:
- `build.poly`: The input build definition.
- `src/app.cpp`: A simple C++ application to be compiled.
- `tests/verify.py`: A Python script that verifies the compiled application.

If your code translation and execution are successful, the Python test script will automatically write a verification output to `/home/user/polybuild/build_success.log`. Leave this file intact for automated verification.