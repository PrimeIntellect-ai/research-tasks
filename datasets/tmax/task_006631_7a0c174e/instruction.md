You are acting as a release manager preparing a new deployment for our internal mathematical evaluation tool, `math_eval`. 

The development team has staged the next release in `/home/user/math_release`. The source code for our Reverse Polish Notation (RPN) mathematical interpreter is located in `/home/user/math_release/src/evaluator.cpp`. However, a critical bug was found in the subtraction logic during the last CI run.

A developer has provided a patch to fix this issue, located at `/home/user/math_release/patch/fix_subtraction.patch`.

Your tasks are:
1. Apply the patch `fix_subtraction.patch` to the source code `evaluator.cpp`.
2. Create a standard `Makefile` in `/home/user/math_release` that defines a `all` target to compile `src/evaluator.cpp` into an executable. The compiled executable MUST be placed at `/home/user/math_release/bin/math_eval`. (You may need to create the `bin` directory). We compile using `g++` with the `-std=c++17` flag.
3. Once built, run the newly compiled `math_eval` interpreter. It reads RPN expressions from standard input (one per line) and prints the result to standard output. Feed it the test cases provided in `/home/user/math_release/tests/inputs.txt`.
4. Redirect the final evaluation output to `/home/user/math_release/deploy_results.log`.

Ensure `deploy_results.log` contains only the numeric results of the evaluated expressions, exactly corresponding to the lines in `inputs.txt`.