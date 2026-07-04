You are a build engineer managing internal artifacts. We have exported a dump of our internal package registry to a custom text format. Your task is to write a script or program to parse this registry, resolve the dependency graph for a specific target package, and generate a strict build plan.

You have access to the registry dump at `/home/user/registry.txt`. 
The file uses a custom multi-line format separating entries with `---`:
```
PKG: <PackageName>
VER: <SemanticVersion>
DEPS: <Comma-separated constraints, or NONE>
---
```
A dependency constraint looks like `PackageName>=1.0.0`, `PackageName==2.1.3`, or `PackageName<3.0.0`. Valid operators are `==`, `>=`, `<=`, `>`, `<`.

Your objective is to resolve the dependency graph for the package `AppX` and determine the exact versions of all packages needed to build it. 

Follow these strict rules for resolution:
1. **Semantic Versioning**: When multiple versions of a package exist in the registry, you must select the *highest* version that satisfies ALL constraints from all dependent packages in the graph. Standard SemVer precedence applies (e.g., 1.2.0 > 1.1.5).
2. **Graph Traversal**: Discover the transitive dependencies of `AppX`. If a package is not required (directly or indirectly) by `AppX`, ignore it.
3. **Build Order (Topological Sort)**: Output the resolved packages such that every package is built *after* its dependencies.
4. **Tie-breaking**: If multiple packages are ready to be built (all their dependencies are already built), order them alphabetically by package name.

Once you have computed the build plan, save it to `/home/user/build_plan.txt`. Each line should contain the resolved package and version in the format `PackageName@Version`.

Example output format:
```
BaseLib@1.0.0
Utils@2.1.0
AppX@1.0.0
```

You may use any programming language (e.g., Python, Bash, Node.js) available in standard Linux environments to write your solution.