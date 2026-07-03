You are an engineer setting up a polyglot build system from scratch. We have a monolithic repository containing various components, and we need a Python script to plan the build process incrementally.

Instead of building everything from scratch every time, we want to only rebuild components that have changed, as well as any components that depend on them (cascading rebuilds). 

Write a Python script at `/home/user/plan_build.py` that accomplishes this.

### Requirements:

1. **Repository Structure**:
   The repository is located at `/home/user/polybuild`. Inside this directory and its subdirectories, there are several `build.json` files. 
   Each `build.json` defines a build target with the following schema:
   ```json
   {
     "name": "<target_name>",
     "deps": ["<dependency_target_1>", "<dependency_target_2>"],
     "cmd": "<build_command>"
   }
   ```

2. **State Caching**:
   There is an existing cache file located at `/home/user/polybuild/cache.json` which maps target names to their last successful build command.
   ```json
   {
     "target_name": "previous_build_command"
   }
   ```

3. **Invalidation Logic**:
   A target is considered "dirty" and must be rebuilt if ANY of the following are true:
   - The target is not present in `cache.json`.
   - The target's current `cmd` in its `build.json` does NOT exactly match the command stored for it in `cache.json`.
   - Any of the target's dependencies (or transitive dependencies) are marked as dirty.

4. **Outputs**:
   Your script `/home/user/plan_build.py` should execute and generate two files:
   
   A) **`/home/user/build_plan.sh`**:
      A bash script containing the build commands (`cmd`) for ONLY the dirty targets, in valid topological order (dependencies must be built before the targets that depend on them). 
      The file must begin with `#!/bin/bash` on the first line, followed by the commands (one per line). Do not include commands for targets that do not need to be rebuilt.

   B) **`/home/user/new_cache.json`**:
      A new JSON file representing the updated cache. It must contain the mapping of `name` to `cmd` for ALL targets currently found in the tree (whether they were dirty or not), so it can be used for the next run. Format this file with standard JSON serialization (e.g., `json.dump`).

Execute your script to produce `/home/user/build_plan.sh` and `/home/user/new_cache.json`. The automated tests will verify the correctness of these two output files.