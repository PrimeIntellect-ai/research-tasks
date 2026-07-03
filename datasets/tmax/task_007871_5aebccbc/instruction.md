You are a platform engineer maintaining a CI/CD pipeline for a complex polyglot monorepo. 

We need to build a custom Python build orchestrator because off-the-shelf tools aren't handling our specific semantic versioning and build-log parsing requirements well. 

Your task is to write a Python script at `/home/user/pipeline/orchestrator.py` that performs the following steps:

1. **Dependency Management & Semantic Versioning**: 
   Read `/home/user/pipeline/packages.json`. This file contains a dictionary of packages. Each package has a list of available `versions` and a `dependencies` dictionary specifying required semver ranges (e.g., `>=1.2.0, <2.0.0`). 
   Implement semver parsing and comparison (you may use the standard library only, no external semver packages) to determine the *latest available version* of each package that satisfies all dependency constraints imposed by other packages.

2. **Custom Data Structure & Build Orchestration**:
   Design a Directed Acyclic Graph (DAG) to represent the package dependencies and perform a topological sort to determine the correct build order. 

3. **State Machine Parser**:
   For each package in the resolved topological order, execute the build script `/home/user/pipeline/mock_builder.sh <package_name> <resolved_version>`.
   Capture the standard output of this script. The output represents a build log containing state transitions and warnings, formatted like:
   `[STATE: <STATENAME>] ...`
   `[WARN: <STATENAME>] ...`
   
   Build a custom state machine parser to process this log. Your parser must count the number of warnings (lines starting with `[WARN: `) that occur *specifically* while the state machine is in the `COMPILING` state. Ignore warnings in `INIT`, `LINKING`, or `DONE` states.

4. **Output Generation**:
   Write a final report to `/home/user/pipeline/report.json` in the following exact format:
   ```json
   {
     "packages": {
       "package_name": {
         "version": "resolved_version_string",
         "compile_warnings": integer_count_of_compiling_warnings
       }
     }
   }
   ```
   The dictionary under `"packages"` should include all packages processed, but the order of keys does not matter.

Constraints:
- Use only standard Python 3 libraries.
- Ensure the orchestrator is executable and runs without errors.