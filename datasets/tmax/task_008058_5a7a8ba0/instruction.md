You are acting as an AI assistant for a web developer who is building a high-performance backend module for calculating complex mathematical expressions. To optimize this, they have decided to implement a minimal Reverse Polish Notation (RPN) Virtual Machine in C. 

The project is located in `/home/user/math_feature`. However, the developer has run into some issues:
1. The `Makefile` in `/home/user/math_feature/` is broken and fails to build the project.
2. Once compiled, the RPN interpreter (written in `/home/user/math_feature/rpn_vm.c`) computes incorrect results for any expressions involving subtraction or division. For example, "10 2 /" should yield 5, but currently does not.

Your task:
1. Fix the `Makefile` so that running `make` successfully builds the executable `rpn_vm`.
2. Debug and fix the `rpn_vm.c` code so that subtraction (`-`) and integer division (`/`) work correctly according to standard RPN evaluation rules.
3. Once fixed and compiled, evaluate the following mathematical expression using the compiled `rpn_vm` program:
   `100 20 5 - / 3 * 7 +`
4. Save the exact numerical output of that expression to a file named `/home/user/math_feature/result.txt`. The file should contain nothing but the final integer result.

Do not use root access or install external packages; everything you need is already in the standard C library and build tools.