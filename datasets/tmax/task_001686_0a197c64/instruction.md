You are acting as a release manager preparing deployments for an internal monorepo. Some of the internal Python packages have broken dependency specifications in their metadata files.

Your task is to write a script in any language you choose to parse package metadata, evaluate version constraints, resolve the dependency graph, and determine a valid build order.

In the `/home/user/packages` directory, you will find several subdirectories. Each subdirectory represents a package and contains a `pkg_info.json` file. 
The `pkg_info.json` files have the following structure:
```json
{
  "name": "package_name",
  "version": "1.2.3",
  "dependencies": {
    "other_package": ">= 1.0.0",
    "another_package": "== 2.1.0"
  }
}
```

Version numbers strictly follow a `MAJOR.MINOR.PATCH` format.
Dependency constraints can use the following operators: `==`, `>=`, `<=`, `>`, `<`. A dependency requirement is specified as a single operator followed by a space and the version number.

Your script must:
1. Parse all `pkg_info.json` files to understand the available packages and their exact versions.
2. Evaluate the dependency expressions to build a directed dependency graph.
3. Identify any packages that have unresolvable dependencies (either the required package does not exist, or the available version does not satisfy the constraint). If a package has an unresolvable dependency, it must be dropped. Any packages that depend on a dropped package must also be dropped (cascading failure).
4. Perform a topological sort on the remaining valid packages to determine a safe build order. 
5. **Tie-breaking rule:** If multiple packages have all their dependencies met and can be built at the same time, sort them alphabetically by their package name.

Outputs required:
1. Create a file at `/home/user/build_order.txt` containing the names of the successfully resolved packages in the correct build order, one package name per line.
2. Create a file at `/home/user/dropped.txt` containing the names of all dropped/unresolvable packages, sorted alphabetically, one package name per line.