You are a build engineer tasked with rescuing a broken legacy Python package. The package metadata (version and dependencies) is missing from its `pyproject.toml`. The original build system used a custom, rudimentary stack-based Domain Specific Language (DSL) to encode and compute metadata dynamically. We only have the leftover `.build_recipe` file, and the original compiler is lost.

Your task is to:
1. Write a Bash script `/home/user/interpreter.sh` that implements an emulator for this stack-based DSL.
2. Execute your interpreter on the recipe to recover the encoded metadata.
3. Fix the `pyproject.toml` using the recovered metadata.
4. Build the Python package into a wheel and store it in an artifacts directory.

**Phase 1: Implement the DSL Interpreter**
Write a Bash script at `/home/user/interpreter.sh`. It must accept a single argument (the path to the DSL script) and execute it line by line. The DSL operates on a single LIFO (Last-In-First-Out) stack of strings.

The interpreter must support the following instructions exactly:
- `PUSH <string>`: Pushes the literal `<string>` onto the top of the stack.
- `CONCAT`: Pops the top value (`val1`), then pops the next value (`val2`), concatenates them as `val2` followed by `val1` (i.e., `val2` + `val1`), and pushes the resulting string back onto the stack.
- `B64DEC`: Pops the top value, decodes it from Base64, and pushes the decoded string back onto the stack.
- `PRINT`: Pops the top value and prints it to standard output (without a trailing newline).

*Note: Your `interpreter.sh` must strictly use Bash, though standard GNU coreutils (like `base64`) are allowed inside it.*

**Phase 2: Extract Metadata**
The legacy package is located at `/home/user/legacy_pkg`. Inside, you will find `/home/user/legacy_pkg/recipe.dsl`.
Run your `interpreter.sh` on `recipe.dsl`. The output will be a JSON string containing the package version and dependencies.
Save this JSON output to `/home/user/metadata.json`.

**Phase 3: Fix Configuration and Build**
Inside `/home/user/legacy_pkg`, there is a `pyproject.toml` file with missing fields marked by `# INSERT_VERSION_HERE` and `# INSERT_DEPS_HERE`.
1. Parse the JSON from Phase 2.
2. Replace `# INSERT_VERSION_HERE` with a valid TOML `version` assignment (e.g., `version = "x.y.z"`).
3. Replace `# INSERT_DEPS_HERE` with a valid TOML `dependencies` assignment (e.g., `dependencies = ["dep1"]`).
4. Build the Python package wheel using `python3 -m build` (install `build` if necessary).
5. Create the directory `/home/user/artifacts/` and move the generated `.whl` file from `/home/user/legacy_pkg/dist/` into `/home/user/artifacts/`.