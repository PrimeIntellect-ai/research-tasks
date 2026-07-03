You are a QA engineer tasked with fixing and testing an internal dependency resolution tool. We have a C program located at `/home/user/qa_env/eval_graph.c` which parses a graph representation of package dependencies. 

The program reads from standard input. Each line contains:
`[Source_Node] [Dest_Node] [Math_Expression]`
(e.g., `pkgA pkgB 2+3*4`)

The program parses the mathematical expression to determine the "weight" (installation time in seconds) of the dependency edge, builds the graph, and calculates the shortest path from a node named `START` to a node named `END` using Dijkstra's algorithm.

However, the build environment is failing because the C program has a critical bug: its recursive descent parser incorrectly evaluates the precedence of multiplication (`*`) and addition (`+`). For example, it evaluates `2+3*4` as `20` instead of `14`.

Your tasks are to:
1. Fix the precedence bug in the expression parser within `/home/user/qa_env/eval_graph.c` so that standard mathematical precedence is respected (multiplication happens before addition). The parser currently only needs to support single-digit integers, `+`, and `*`. Parentheses are not supported.
2. Compile the fixed program to `/home/user/qa_env/eval_graph` using `gcc`.
3. Implement a property-based testing script in bash at `/home/user/qa_env/prop_test.sh` that validates the math parser. The script must randomly generate at least 50 test cases of valid math expressions (using single digits, `+`, and `*`), feed them as a single-edge graph (`START END <expr>`) to your compiled `eval_graph` program, and compare the shortest path output against the system's `bc` command. If any test fails, the script should exit with a non-zero status.
4. Once your program passes your property-based tests, run it against the official dependency graph provided at `/home/user/qa_env/prod_graph.txt`.
5. Create a file at `/home/user/qa_report.txt` containing exactly the integer representing the shortest path cost from `START` to `END` in `prod_graph.txt`.

Ensure your C code handles the fixes elegantly and your bash script is entirely self-contained, using standard tools like `awk`, `sed`, `bc`, or `$RANDOM`.