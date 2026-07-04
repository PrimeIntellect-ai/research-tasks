You are an engineer porting a legacy configuration evaluation tool to work in a minimal Linux container environment. The original tool, written in Rust, had strict ownership and borrow checking semantics for variable evaluation. Since we cannot install the Rust toolchain in this minimal container, you need to write a standalone Python replacement.

Your task is to create a Python script at `/home/user/evaluator.py` that parses a directory of mathematical expressions, resolves their dependencies, and evaluates a target variable while enforcing a simulated "borrow checker" limit.

The expressions are stored in `.expr` files in a given directory. Each file contains exactly one assignment of the form:
`VAR = expression`
Where `expression` can contain integer literals, other variable names, parentheses, and standard arithmetic operators (`+`, `-`, `*`, `/` for integer division).

Your script must be invoked as:
`python3 /home/user/evaluator.py <directory_path> <target_variable>`

Requirements:
1. **Expression Parsing & Evaluation**: Parse the expressions and evaluate the final integer value of the `<target_variable>`. Use standard Python integer math.
2. **Dependency Resolution**: Variables may be defined in any `.expr` file in the directory (the filename matches the variable name, e.g., `A.expr` defines `A`). You must recursively resolve and evaluate dependencies required to compute the target.
3. **Circular Dependency Detection**: If evaluating the target encounters a circular dependency in the graph, the script must print exactly `CircularDependency` to stdout and exit with status code `2`.
4. **Simulated Borrow Checker (Ownership limit)**: In the spirit of the original Rust tool, a variable's value can only be "borrowed" (read) a maximum of 2 times during the entire evaluation of the target variable. If computing the target requires reading any variable 3 or more times across all evaluated expressions, the script must print exactly `OwnershipError: <VAR_NAME>` to stdout (where `<VAR_NAME>` is the variable that exceeded the read limit) and exit with status code `1`. Note: Only count reads of variables that are actually evaluated while computing the target.
5. **Success**: If evaluation succeeds without violating the borrow limit or cycles, print exactly `Result: <value>` to stdout and exit with status code `0`.

Examples of borrow counting:
If `A = B + C`, `B = D * 2`, and `C = D + 3`, and we evaluate `A`, variable `D` is read 2 times. This is valid.
If we had `A = B + C + E`, `B = D`, `C = D`, `E = D`, then evaluating `A` reads `D` 3 times. This violates the limit.

Write the script `/home/user/evaluator.py` robustly. The environment already contains python3.