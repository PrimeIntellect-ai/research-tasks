You are tasked with setting up the core engine of a new polyglot build orchestrator. The build orchestrator needs to parse a dependency graph, calculate the computational "weight" of each task by evaluating a mathematical expression, and then execute these tasks concurrently using Go.

You need to write a Go program `/home/user/builder.go` and a CI pipeline script `/home/user/ci.sh`.

**1. The Build Orchestrator (`/home/user/builder.go`)**
Write a Go program that reads a build configuration file located at `/home/user/polygraph.txt`. 
Each line in this file defines a build task in the following format:
`TaskName : Dependency1,Dependency2 : CostExpression`
(Note: Dependencies are comma-separated and may be empty if the task has no dependencies. Spaces around the colons and commas can vary).

Example `polygraph.txt` lines:
```
setup_env : : 3 + 5 * 2
compile_c : setup_env : 20 / 4 + 1
compile_go : setup_env : 15 - 5
link : compile_c,compile_go : 10 + 2 * 3
```

Your Go program must:
1. Parse the file and extract the tasks, dependencies, and cost expressions.
2. Implement an expression parser and evaluator to calculate the integer result of the `CostExpression`. The expressions will only contain non-negative integers and the operators `+`, `-`, `*`, `/`. You must honor standard mathematical order of operations (multiplication and division take precedence over addition and subtraction).
3. Execute the tasks concurrently using Go's concurrency primitives (goroutines, channels, waitgroups, etc.). 
   - A task cannot start until ALL of its dependencies have finished.
   - Tasks that have their dependencies met must run concurrently.
   - To simulate the task execution, the program should sleep for `W` milliseconds, where `W` is the evaluated integer result of the task's cost expression.
4. Log the execution steps to a file exactly at `/home/user/build_log.txt`.
   - When a task starts, append the line: `START <TaskName> <Weight>` (e.g., `START setup_env 13`)
   - When a task finishes, append the line: `DONE <TaskName>` (e.g., `DONE setup_env`)

**2. The CI Script (`/home/user/ci.sh`)**
We need a simple local CI/CD script to build, profile, and verify the orchestrator.
Create a bash script at `/home/user/ci.sh` that:
1. Compiles `/home/user/builder.go` into an executable named `builder` in the same directory.
2. Runs the compiled `builder` executable.
3. Your Go program must be configured to generate a CPU and Memory profile upon successful execution. Ensure the script triggers the Go program in a way that generates a memory profile saved exactly to `/home/user/mem.prof`. (You will need to implement the profiling hooks in `builder.go` using `runtime/pprof` or similar).

**Constraints:**
- Use Go as the language for the orchestrator. Standard library only; do not download external modules for expression parsing.
- Assume `/home/user/polygraph.txt` will be present before your program runs.
- Ensure the CI script is executable (`chmod +x /home/user/ci.sh`).
- If a dependency doesn't exist, the build should fail, but you can assume the provided graph is a valid, acyclic graph.