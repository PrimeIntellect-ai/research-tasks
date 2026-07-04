You are a mobile build engineer maintaining a CI pipeline. Recently, a script generating reverse proxy configurations for our testing environment started failing in CI. While the script runs fine locally sometimes, it intermittently fails in CI due to the ordering of the generated configuration lines caused by background processes.

Furthermore, the binary used to calculate the proxy weights, `eval`, was accidentally deleted from the repository. You must recreate it and fix the script.

**Your objectives:**
1. **Write the Math Evaluator**: Create a C program at `/home/user/eval.c` that acts as an emulator/interpreter for a simple Reverse Polish Notation (RPN) mathematical language. 
    * It must accept a single string argument containing space-separated tokens.
    * Supported operators: `+` (add), `-` (subtract), `*` (multiply), `/` (integer divide).
    * Operands are strictly positive integers.
    * The program should evaluate the RPN expression, print the final integer result to `stdout` (with a newline), and exit.
    * Compile it to `/home/user/eval` using `gcc`.

2. **Fix the CI Script**: The script `/home/user/test.sh` runs `eval` concurrently to calculate weights for different reverse proxy backends. Because of the concurrent background execution (`&`), the order of the appended lines in `/home/user/proxy.conf` is non-deterministic, causing CI pipeline failures that expect strict ordering.
    * Modify `/home/user/test.sh` so that it still performs the calculations, but guarantees that `backend1`'s configuration line is always written *before* `backend2`'s configuration line in `/home/user/proxy.conf`.
    * Ensure the script handles concurrency safely without interleaving output.

3. **Generate the Configuration**: Run your fixed `/home/user/test.sh` to generate the final `/home/user/proxy.conf`.

**Constraints:**
* Use standard C libraries. 
* Do not remove the concurrency (the subshells or backgrounding logic) from the evaluation steps in `test.sh`; fix the synchronization/ordering of the file writing instead.