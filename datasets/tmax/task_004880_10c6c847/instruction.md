You are an AI assistant helping a computational biology researcher run a simulation to optimize a DNA primer sequence. 

I have a C++ file at `/home/user/primer_sim.cpp` that simulates primer binding against a target sequence using a Monte Carlo method (introducing random SNPs to simulate sequence variations). The function `score_primer(std::string primer)` calculates the average alignment score over 100 Monte Carlo iterations.

However, the optimization function `find_best_primer()` is incomplete. I need you to implement a stochastic hill-climbing optimization algorithm inside this function to find the optimal 10-mer primer.

Here is the exact algorithm you must implement in `find_best_primer()` to ensure reproducibility:
1. Initialize the current primer as `"AAAAAAAAAA"`.
2. Evaluate its initial score using `score_primer()`.
3. Initialize a local random number generator: `std::mt19937 local_gen(123);`
4. Define the possible bases as an array: `const char bases[] = {'A', 'C', 'G', 'T'};`
5. Run a loop for exactly **500 iterations**. In each iteration:
   a. Create a mutated primer by copying the current primer.
   b. Select an index to mutate: `int idx = local_gen() % 10;`
   c. Select a new base: `int base_idx = local_gen() % 4;`
   d. Assign the new base to the mutated primer: `mutated[idx] = bases[base_idx];`
   e. Evaluate the mutated primer using `score_primer()`.
   f. If the new score is **greater than or equal to** the current score, update the current primer and the current score to the mutated versions.
6. Return the current primer after 500 iterations.

Your task:
1. Edit `/home/user/primer_sim.cpp` to implement this logic.
2. Compile the C++ code using `g++ -O3 -std=c++11 /home/user/primer_sim.cpp -o /home/user/primer_sim`.
3. Run the compiled executable `/home/user/primer_sim`.

The program will automatically create a file at `/home/user/best_primer.txt` containing the optimized primer and its score. I will verify this file.