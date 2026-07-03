You are an AI assistant acting as a build engineer managing multi-language artifacts.

We have a set of packages and their dependencies defined in `/home/user/deps.json`. The keys are package names, and the values are lists of packages they depend on.
We also have an SQLite database `/home/user/artifacts.db` that contains a `packages` table with metadata about these packages. 

Your task is to write and execute a Python script at `/home/user/build_mgr.py` that does the following:

1. **Schema Migration**: Connect to `/home/user/artifacts.db` and add a new column named `build_order` of type `INTEGER` to the `packages` table.
2. **Dependency Resolution**: Read `/home/user/deps.json` and perform a topological sort to determine the correct build order. A package can only be built after all its dependencies have been built. 
   *Tie-breaking rule*: If multiple packages are ready to be built at the same time, pick the package name that comes first alphabetically.
3. **Database Update**: Update the `build_order` column in the `packages` table for each package. Use a 1-based index (i.e., the first package to be built gets `build_order = 1`, the second gets `2`, and so on).
4. **Mock Test Fixtures**: For each package in the resolved build order, create a mock artifact file in the directory `/home/user/artifacts/` (create the directory if it doesn't exist). The file should be named `<package_name>.mock` and its content must be exactly `MOCK_BUILD_<package_name>`.

Please write the script and run it so that the database and the file system are updated to the required final state.