You are an open-source maintainer reviewing a broken Pull Request. 

A contributor submitted a patch (`feature-factorial.patch`) to our C-based Reverse Polish Notation (RPN) calculator project located in `/home/user/rpn_calc`. The PR is supposed to add a factorial operator `!`. 

However, the CI pipeline is failing because of a linking error, and the contributor also mentioned the math output seems incorrect during their local tests. 

Your task is to:
1. Apply the patch `feature-factorial.patch` to the source code.
2. Fix the build system configuration in the `Makefile` so that the project compiles and links correctly.
3. Fix the logical mathematical error in the newly added C file.
4. Compile the project by running `make`.
5. Run the newly compiled calculator (`./calc`) to calculate the factorial of 5, and then print it. Save the exact output of this operation to `/home/user/calc_out.txt`.

The calculator reads space-separated tokens from standard input and processes them using a custom stack data structure. The token `P` pops and prints the top value of the stack. For example, to add 3 and 4, you would use: `echo "3 4 + P" | ./calc`.

Ensure your final compiled executable is located at `/home/user/rpn_calc/calc` and the output file is `/home/user/calc_out.txt`.