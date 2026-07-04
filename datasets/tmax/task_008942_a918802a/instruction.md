You have just inherited an unfamiliar, undocumented utility for a sensor system. The source code is located at `/home/user/calibrator.c`. 

The original developer mentioned that it calculates a recursive baseline sum and extracts signal roots, but it currently fails to execute properly. From user reports, the binary either crashes, hangs indefinitely, or triggers stack overflows when run. 

Your task is to debug and fix `/home/user/calibrator.c`. Based on initial triage, there are three distinct logical issues in the code:
1. A recursive function that fails to terminate properly.
2. A mathematical convergence condition that causes an infinite loop due to improper floating-point comparison. You should allow a tolerance of `0.0001` for the loop's exit condition.
3. A memory corruption issue caused by a boundary condition / off-by-one error when populating the output array.

Instructions:
1. Identify and fix the three bugs in `/home/user/calibrator.c`.
2. Compile the fixed C program into an executable named `/home/user/calibrator`. Use `gcc -o /home/user/calibrator /home/user/calibrator.c -lm`.
3. Run the compiled executable and redirect its standard output to `/home/user/calibration_output.txt`.

Do not change the initial input data array (`10, 20, 30, 40, 50`) or the formatting of the `printf` statements. The success of this task will be verified entirely by checking the precise contents of `/home/user/calibration_output.txt`.