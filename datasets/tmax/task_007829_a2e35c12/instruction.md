You are a developer tasked with automating the resolution of dependency conflicts in a legacy Rust project. The compilation currently fails due to outdated dependencies in the `Cargo.toml` file.

We have exported the compilation errors to a log file and the local crate registry to a JSON file. 

Your task is to write a Python script at `/home/user/fix_deps.py` that analyzes the logs, finds the correct package versions, and generates a patch file to fix the `Cargo.toml`.

**Available Files:**
1. `/home/user/Cargo.toml`: The broken project manifest.
2. `/home/user/build_errors.log`: A custom log containing multiline error blocks.
3. `/home/user/registry.json`: A JSON file mapping package names to lists of available semantic versions.

**Requirements for `/home/user/fix_deps.py`:**
1. **State Machine Parser**: Read `/home/user/build_errors.log` using a state machine approach to extract dependency conflicts. Conflict blocks always start with `-- BEGIN CONFLICT --`, followed by `Package: <name>` and `Constraint: <operator><version>` (e.g., `>=1.10.0`, `>1.0.5`), and end with `-- END CONFLICT --`.
2. **Serialization**: Load `/home/user/registry.json`.
3. **Semantic Version Comparison**: For each conflicting package, find the available versions in the registry that satisfy the parsed constraint. 
   - You must select the **highest** available semantic version that satisfies the constraint BUT has the **same MAJOR version** as the version specified in the constraint.
   - Standard SemVer rules apply (e.g., `1.10.0` > `1.9.0`).
4. **Diffing**: Read `/home/user/Cargo.toml`. Replace the old version strings of the conflicting packages with the new versions you computed. Generate a unified diff patch between the original `Cargo.toml` and the fixed version. 
5. **Output**: Save the generated unified diff to `/home/user/cargo.patch`. The patch must be applicable directly to the original `Cargo.toml` (e.g., header paths should be `--- Cargo.toml` and `+++ Cargo.toml`).

Write the Python script, execute it, and ensure `/home/user/cargo.patch` is created with the correct diff. Do not use any external Python libraries (only standard library modules like `json`, `difflib`, `re`, etc.).