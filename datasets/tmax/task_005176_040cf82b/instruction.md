You are an integration developer tasked with building a tool to resolve package dependencies from a mock API response. You have received an API dump containing a package dependency graph with conflicting constraints, and you need to find a globally valid resolution that minimizes the total "cost" of the chosen versions.

The API response is located at `/home/user/api_dump.json`. It is a JSON file with three top-level keys:
1. `"packages"`: A dictionary where each key is a package name, and the value is a list of available versions for that package. Each version object contains `"version"` (a string like "1.0") and `"cost"` (a float representing the integration cost).
2. `"dependencies"`: A dictionary defining the dependencies for specific package versions. The keys are formatted as `"PackageName@Version"` (e.g., `"A@1.2"`). The value is a list of requirement objects, each specifying `"package"` (the required package name), `"min_version"`, and `"max_version"`.
3. `"root"`: An object specifying the entry point for your resolution, containing `"package"`, `"min_version"`, and `"max_version"`.

Your task:
Write a Python script at `/home/user/resolve.py` that processes this JSON and finds a valid assignment of versions to packages such that:
- The `root` package is included and its chosen version satisfies the root `min_version` and `max_version` constraints.
- For every package version included in the resolution, all its dependencies (as defined in `"dependencies"`) are also included.
- For any included dependency, the chosen version of that package must satisfy the `"min_version"` and `"max_version"` constraints specified by the depender.
- A package can only have **one** version chosen globally. If multiple packages depend on the same package (e.g., `B` and `C` both depend on `D`), the single chosen version for `D` must satisfy the constraints of both `B` and `C`.
- Versions should be compared lexicographically (or parsed as floats, since they are all in "X.Y" format). A version satisfies the constraint if `min_version <= version <= max_version`.
- The total cost (sum of the `"cost"` values of all chosen package versions) must be **minimized**.
- Assume that unmentioned dependencies for a specific package version mean it has no further dependencies.

After finding the optimal resolution, your script should:
1. Write the minimum total cost as a formatted float (2 decimal places) to `/home/user/min_cost.txt`.
2. Write the final version assignment to `/home/user/resolution.json` as a dictionary mapping package names to their chosen version strings (e.g., `{"A": "1.2", "B": "2.0", ...}`).

Run your script to produce these output files.