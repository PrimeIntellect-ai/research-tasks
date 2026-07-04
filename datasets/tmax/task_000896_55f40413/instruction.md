You are an integration developer responsible for building a dependency resolution tool in Bash. 
In your environment, there is a package registry represented as a JSON file at `/home/user/registry.json`. 

Your task is to write a Bash script that traverses the dependency graph for a few specific target applications, satisfies all version constraints, and determines the exact set of package versions needed for each target. 

The dependency constraints in the JSON use three operators: `==`, `>=`, and `<=`. 
If multiple versions of a dependency satisfy all constraints in the tree, you must select the **highest** compatible version. The versioning follows semantic versioning (Major.Minor.Patch).

You need to resolve the full transitive dependencies for the following three targets:
1. `app_alpha@1.0.0`
2. `app_beta@2.1.0`
3. `app_gamma@3.0.0`

Once resolved, write the results to a file named `/home/user/resolutions.txt`.

The format of `/home/user/resolutions.txt` must be exactly as follows for each target:
```
[target_name@version]
packageA@version
packageB@version
...
```
The dependencies for each target must be listed in **alphabetical order** by package name. Each target section should be separated by a single newline. Include the target application itself in the list if it's considered a package (for these targets, just list their resolved dependencies including themselves if you treat them as nodes, but to be precise: output the target itself in the list).

Example output format:
```
[app_alpha@1.0.0]
app_alpha@1.0.0
lib_core@1.2.0
lib_net@2.0.1

[app_beta@2.1.0]
app_beta@2.1.0
lib_auth@1.0.0
lib_core@1.2.0
```

Constraints:
- You must use Bash (`jq` is available and recommended for parsing the JSON).
- You can create helper scripts in Bash, Python, or Perl if needed, but the primary orchestration should be accessible from the terminal. 
- Ensure your constraints solver correctly backtracks or intersects constraints if two packages depend on the same underlying library with different version constraints.

System setup:
- The registry file is located at `/home/user/registry.json`.