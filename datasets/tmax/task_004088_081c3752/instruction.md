You are acting as a data scientist evaluating a simple risk model using a Monte Carlo approach. You need to write a simulation in C++ and a Bash script to orchestrate a convergence test, summarizing the outputs.

**Background Model:**
A gambler starts with a capital of $S_0 = 10$. 
They play a game for up to 100 steps. 
At each step, they win $1 with probability 0.45, and lose $1 with probability 0.55.
If their capital $S$ reaches $0$, they are "ruined", and the game immediately ends for that simulation.

**Step 1: Write the C++ Simulator**
Create a C++ program at `/home/user/mc_ruin.cpp`.
It must accept exactly two command-line arguments: `N` (the number of simulations) and `seed` (the random seed).
To ensure exact deterministic behavior across compilers, initialize a Mersenne Twister engine (`std::mt19937 gen(seed);`). At each step, simulate the game using modulo arithmetic: a win occurs if `gen() % 100 < 45`.
The program should run $N$ independent simulations.
It must print ONLY the estimated probability of ruin (a floating-point number, i.e., `ruined_count / N`) to standard output. Do not print any other text.

**Step 2: Orchestrate the Convergence Test**
Write a bash script at `/home/user/run_convergence.sh`.
This script must:
1. Compile `/home/user/mc_ruin.cpp` into an executable named `/home/user/mc_ruin` using `g++` (use `-O3` for performance).
2. Execute the compiled program for three different values of $N$: `1000`, `10000`, and `100000`. Use a fixed seed of `42` for all three runs.
3. Write the results to a file at `/home/user/convergence_report.md`.

The `/home/user/convergence_report.md` file must contain exactly three lines, one for each $N$, strictly following this format:
`N=<N>, P=<probability>`

Example of the expected format in `convergence_report.md`:
`N=1000, P=0.1234`
`N=10000, P=0.12345`

Please execute the bash script to generate the final `convergence_report.md` file.