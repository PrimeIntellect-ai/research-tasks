I have a messy project folder located at `/home/user/math_project`. It contains two C source files: `main.c` and `math_ops.c`. The `math_ops.c` file contains a mathematical numerical algorithm that uses functions from the standard math library, and `main.c` calls it. 

I need you to write a Bash script at `/home/user/math_project/run_pipeline.sh` that performs the following steps to organize the project, fix the build orchestration, benchmark the algorithm, and encode the results:

1. Create three directories inside `/home/user/math_project`: `src`, `bin`, and `results`.
2. Move all `.c` files from `/home/user/math_project` into the `src` directory.
3. Compile the C files into an executable named `calc` located in the `bin` directory. Note: Previous attempts to compile this failed with a linking error related to missing math symbols. You must ensure the correct linker flags are used to resolve standard math library dependencies.
4. Run the compiled `calc` executable with the argument `5000000` (which dictates the number of iterations for the numerical algorithm).
5. Benchmark the execution of the `calc` command using the `time -p` command. Redirect the standard error of the `time -p` command (which contains the real, user, and sys times) to a file at `/home/user/math_project/results/benchmark.txt`.
6. Take the standard output of the `calc` executable, encode it using `base64`, and save the encoded string to `/home/user/math_project/results/encoded_out.b64`.

Ensure your script is executable (`chmod +x`). Do not run the script yourself; I will run it to verify your work.