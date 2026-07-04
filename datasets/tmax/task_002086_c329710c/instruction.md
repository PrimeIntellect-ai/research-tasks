You are an AI assistant helping a developer organize project files and dependencies. We have a mathematical dependency resolver originally prototyped in Python, but it's currently broken and we want to rewrite it entirely in Go for better performance and type safety.

The task is to write a Go program that solves a constraint satisfaction problem to find the optimal set of packages to install. 

**Your Environment:**
Workspace: `/home/user/workspace`

**Problem Statement:**
You have a set of packages. Each package has a `size` (integer), a list of `depends_on` (other packages that MUST be installed if this one is), and a list of `conflicts_with` (packages that CANNOT be installed if this one is).

You must write a Go program that reads a `/home/user/workspace/packages.json` file. The JSON format is a dictionary where the key is the package name and the value is an object containing `size`, `depends_on`, and `conflicts_with`.

**Goal:**
Find a valid subset of packages to install that satisfies all these conditions:
1. It MUST include the package named `"core-app"`.
2. For every package in the subset, all its `depends_on` packages must ALSO be in the subset.
3. For every package in the subset, NONE of its `conflicts_with` packages can be in the subset.
4. The sum of the `size` of all packages in the subset must be less than or equal to `120`.
5. **Optimization Objective 1:** Maximize the *number* of packages in the subset.
6. **Optimization Objective 2:** If there is a tie in the number of packages, maximize the total *size* of the subset.

**Requirements:**
1. **Initialize a Go module:** Create a module named `mathpack` in `/home/user/workspace`.
2. **Implementation:** Write the solver in `/home/user/workspace/solver.go`. It should read `packages.json`, solve the constraint problem, and write the resulting list of package names as a JSON array of strings (sorted alphabetically) to `/home/user/workspace/install_plan.json`.
3. **Testing:** Write unit/integration tests in `/home/user/workspace/solver_test.go` that verify your constraint satisfaction logic on at least one mock dataset.
4. **Execution:** Run your tests using `go test`, and then run your program to generate `install_plan.json`.

Ensure your Go code is well-structured, compiles without errors, and correctly implements the constraints.