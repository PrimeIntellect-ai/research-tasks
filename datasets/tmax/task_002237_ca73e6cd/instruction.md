You are an open-source maintainer reviewing a pull request for a custom package management system. Historically, this system relied on a proprietary, closed-source binary tool to resolve package dependencies, evaluate semantic versions, and detect circular imports. The community has submitted a PR to replace this slow binary with a new C++ implementation, but it's currently broken.

Your task is to fix the C++ implementation located in `/home/user/resolver_pr/` so that it flawlessly replaces the legacy binary.

**The Legacy Oracle:**
We have shipped the stripped, proprietary binary at `/app/legacy_resolver`. 
Usage: `/app/legacy_resolver <input_file>`
It reads a package dependency graph and outputs either a valid topological installation order, `UNSATISFIABLE`, or `CIRCULAR_DEPENDENCY`. 

**Input Format:**
The input file contains multiple package definitions separated by blank lines.
```text
PKG MyApp 1.2.3
REQUIRES (LibA (>= 1.0.0) AND LibB (< 2.0.0-alpha.1)) OR LibC (= 1.5.0)

PKG LibA 1.0.5
REQUIRES None

PKG LibB 1.9.9
REQUIRES LibA (>= 1.0.0)
```
*   `PKG <Name> <SemVer>` declares a package.
*   `REQUIRES <Expression>` declares dependencies using boolean logic (`AND`, `OR`, `()`) and SemVer constraints (`>=`, `<=`, `>`, `<`, `=`).

**The PR Codebase (`/home/user/resolver_pr/`):**
The contributor provided a basic structure but failed in several areas:
1.  **Expression Parsing:** The recursive descent parser in `parser.cpp` fails on nested parentheses.
2.  **SemVer Comparison:** The logic in `semver.cpp` doesn't strictly follow SemVer 2.0.0 rules for pre-release tags (e.g., `1.0.0-alpha < 1.0.0`).
3.  **State Machine / Cycle Detection:** The cycle detection algorithm gets stuck in infinite loops on certain circular imports (similar to a notorious Go module bug).

**Your Objectives:**
1.  Debug and rewrite the necessary C++ components in `/home/user/resolver_pr/` using standard C++17 or C++20.
2.  Your compiled binary must be saved at `/home/user/fast_resolver`.
3.  Your binary must take exactly one argument (the input file path) and print output identically to `/app/legacy_resolver`.
4.  **Performance:** The legacy resolver is extremely slow. Your C++ implementation must be highly optimized. You are expected to achieve a significant speedup over the legacy binary (at least 20x faster) on large graphs.

Use `/app/legacy_resolver` to test your logic on edge cases. You must ensure 100% output equivalence and meet the performance threshold.