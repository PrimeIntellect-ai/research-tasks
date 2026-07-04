You are a build engineer managing a legacy system's compilation artifacts. The artifact metadata is stored in JSON files located in the `/home/user/artifacts/` directory.

Recently, the team introduced a new schema for these metadata files, but some files have not been migrated yet. Additionally, a bad commit introduced a dependency cycle that breaks the build order.

Your tasks are to:

1. **Schema Migration**: Update all version 1 schemas in `/home/user/artifacts/` to version 2 in-place.
   - Version 1 schema uses `"schema_version": 1` and lists dependencies under the key `"needs"`.
   - Version 2 schema uses `"schema_version": 2` and lists dependencies under the key `"requires"`.
   - You must rename the `"needs"` key to `"requires"` and update `"schema_version"` to `2` for any v1 file. Preserve all other keys.

2. **Fix Dependency Cycle**: There is a known dependency cycle involving `libD`. `libD` mistakenly requires the symbol `"C"`, which creates a circular dependency. Manually or programmatically patch `/home/user/artifacts/libD.json` so that its `"requires"` array contains `"A"` instead of `"C"`.

3. **Dependency Resolution**: Write a Python script to compute the correct build order (topological sort) of the artifacts based on their metadata. 
   - An artifact is ready to build when all the symbols listed in its `"requires"` array are provided by already-built artifacts.
   - Each artifact lists the symbols it provides in its `"provides"` array.
   - If multiple artifacts are ready to be built at the same time, break ties by sorting their `"name"` fields alphabetically.

4. **Output Verification**: Save the final build order (just the `"name"` of each artifact, one per line) to `/home/user/build_order.txt`.

Ensure your Python script runs cleanly and generates the correct output file.