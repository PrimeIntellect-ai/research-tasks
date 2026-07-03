You are helping a developer who is migrating a legacy Python 2 data pipeline to Python 3. The old pipeline relied heavily on an undocumented, pre-compiled C extension for heavy numerical computations over dependency graphs. The source code for this extension is lost. 

To future-proof the system, the team has decided to replace this black-box binary with a standalone Go CLI tool that the new Python 3 pipeline will invoke. 

You have been provided with the extracted, stripped legacy binary at `/app/calc_engine`. 

Your task is to write a Go program that behaves **exactly** like `/app/calc_engine`. You must build your Go program and output the compiled executable to `/home/user/engine/bin`.

### Domain Knowledge: Algorithm and Formats
By inspecting the old Python 2 wrapper code, the team has figured out the input and output formats the binary expects via `stdin` and `stdout`.

**Input Format (Standard Input):**
The input represents a Directed Acyclic Graph (DAG) of numerical operations.
1. The first line contains two integers: `V` (number of vertices/nodes) and `E` (number of directed edges).
2. The next `V` lines describe the nodes. Each line contains:
   `node_id operation [optional_value]`
   - `node_id`: An integer from `0` to `V-1`.
   - `operation`: One of `INPUT`, `ADD`, `MUL`, `MAX`.
   - `optional_value`: A floating-point number, present **only** if the operation is `INPUT`.
3. The next `E` lines describe the directed edges. Each line contains:
   `from_id to_id`
   This means the output of node `from_id` is an input to node `to_id`.

**Evaluation Rules:**
- The graph must be evaluated in topological order.
- `INPUT` nodes evaluate to their `optional_value`.
- `ADD` nodes evaluate to the sum of the values of all incoming edges. (If no incoming edges, evaluates to `0.0`).
- `MUL` nodes evaluate to the product of the values of all incoming edges. (If no incoming edges, evaluates to `1.0`).
- `MAX` nodes evaluate to the maximum value among all incoming edges. (If no incoming edges, evaluates to `-999999.0`).

**Output Format (Standard Output):**
The program must print the final evaluated float value of **every** node in ascending order of `node_id`.
Each line must be formatted as:
`<node_id> <value>`
The floating point value must be formatted to exactly 4 decimal places (e.g., `3.1416`).

### Requirements:
1. Implement the solution in Go.
2. We highly recommend you write a short test orchestrator/fuzzer locally to test your Go implementation against the `/app/calc_engine` oracle on random DAGs before considering the task complete.
3. Save your Go source code in `/home/user/engine/` and compile the final executable exactly to `/home/user/engine/bin`. The automated verifier will blast your binary with thousands of random DAGs and assert bit-exact stdout equivalence with the legacy oracle.