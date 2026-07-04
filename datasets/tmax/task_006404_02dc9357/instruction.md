You are a performance engineer tasked with profiling a prototype C++ bioinformatics application. This application, `align_calc.cpp`, is designed to analyze primer sequence alignments by computing probability distribution distance metrics (specifically Kullback-Leibler divergence), performing numerical integration over a continuous distribution model, and executing a statistical hypothesis comparison to determine if the sequence matches a target profile.

The source code for the application is located at `/home/user/align_calc.cpp`. 

Your task is to:
1. Compile the C++ application from source in a way that allows it to be profiled with `gprof`. Name the compiled executable `align_calc` and place it in `/home/user/`.
2. Run the executable. It does not require any command-line arguments and will generate profiling data (e.g., `gmon.out`) in the current directory upon completion.
3. Use `gprof` to analyze the profiling data and identify the name of the function that consumes the highest percentage of total runtime (the most expensive function in the flat profile, excluding `main`).
4. Write the exact name of this bottleneck function into a text file at `/home/user/bottleneck_function.txt`. The file should contain only the function name (e.g., `compute_kl_divergence`) and nothing else.

Note: You can assume standard build tools (`g++`, `gprof`) are available in the environment.