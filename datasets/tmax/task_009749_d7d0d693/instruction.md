You have inherited an unfamiliar codebase for a mathematical project located in `/home/user/math_project`. The system is designed to calculate the sum of the square roots of a sequence of numbers. 

However, the project is currently broken. When you try to run the main script `./run_math.sh`, it fails. 

Your goals are to diagnose and fix the issues so that `./run_math.sh` successfully executes and produces the correct output in `/home/user/math_project/result.txt`.

Here is what you need to do:
1. **Recover the Missing Data**: The input file `data.txt` was accidentally deleted from the directory. You must recover it. The project is a git repository, and the file was present in a previous commit.
2. **Fix the Build Failure**: The build script `build.sh` attempts to compile a C helper program (`calculate.c`), but it is failing due to a compiler/linker error. Diagnose and fix `build.sh`.
3. **Fix the Crash**: Even after compiling successfully, the `calculate` program crashes with a segmentation fault (core dump) when processing `data.txt`. Use debugging tools to analyze the crash, identify the flaw in `calculate.c`, and fix the code.
4. **Run the Project**: Once the data is recovered and the code is fixed and built, execute `./run_math.sh`. It will automatically run the build script and the calculation. 

Verify that `/home/user/math_project/result.txt` is created and contains the correct sum format: `Sum: <value>`.

Do not change the mathematical logic or the output format of the C program. Only fix the bugs causing the build failure and the segmentation fault.