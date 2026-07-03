You are an engineer working on a C-based CGI module used for parsing secure mathematical tokens in HTTP headers (a Web Security component). The project is located in `/home/user/secure-parser`.

Currently, the project fails to compile due to several issues:
1. **Header Dependency Cycle:** The header files (`ast.h`, `lexer.h`, and `parser.h`) have a circular include dependency that causes compilation to fail even with include guards. You must resolve this cycle (e.g., using forward declarations) so they compile cleanly.
2. **Memory/Lifetime Error:** `evaluate.c` contains a function `int* evaluate_ast(ASTNode* node)` that mistakenly returns a pointer to a stack-allocated local variable. Since the `Makefile` uses `-Werror`, this halts compilation. Fix it by dynamically allocating the returned integer using `malloc`.
3. **Missing Mock for Test Fixture:** The file `test_mock.c` acts as the test fixture but lacks the implementation for an external dependency `int get_secret_key()`. You must implement this function inside `test_mock.c` using **x86_64 inline assembly** to return the value `42`. (Hint: use an `__asm__` block to set the return register or output operand). 
4. **Test Implementation:** In `test_mock.c`, write the `main` function to:
    - Create a mock AST node (type: `ADD`, left value: 10, right value: 5).
    - Call `evaluate_ast` on this node.
    - Add the result of `get_secret_key()` to the evaluated AST result.
    - Print the final integer sum to standard output in the format: `Token: <sum>`

Once you have fixed the code, run `make` in `/home/user/secure-parser` to build the `test_runner` executable. 
Finally, execute `./test_runner` and redirect its output to `/home/user/result.log`.

Do not modify the `Makefile`. Ensure your changes do not introduce memory leaks where possible, though the test runner's exit code is the primary success metric.