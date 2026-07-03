You are a bioinformatics analyst tasked with developing a C++ pipeline to design PCR primers, verify their specificity against a reference genome, and simulate the PCR amplification kinetics using an Ordinary Differential Equation (ODE).

Your task spans from writing the C++ code to compiling and running it using standard Linux CLI tools. 

Here are the specific requirements:

1. **Input Files (Already exist):**
   - `/home/user/target.fasta`: Contains a single DNA sequence (the target to be amplified).
   - `/home/user/reference.fasta`: Contains a larger background DNA sequence.

2. **Primer Design & Alignment:**
   - Extract the Forward Primer: The first 20 nucleotides of the sequence in `target.fasta`.
   - Extract the Reverse Primer: The reverse complement of the last 20 nucleotides of the sequence in `target.fasta`.
   - Search `reference.fasta` for exact substring matches of both the Forward Primer and the Reverse Primer.
   - If either primer appears more than *once* in `reference.fasta`, your program must terminate and write `ERROR: NON-SPECIFIC PRIMERS` to the output log.

3. **ODE Numerical Solving (PCR Simulation):**
   If the primers are specific (appear exactly once in the reference), simulate the PCR amplification using the following logistic growth ODE:
   `dA/dc = r * A * (1 - A / K)`
   Where:
   - `A` = Number of amplicons (initial value at cycle 0 is `A_0 = 10.0`)
   - `c` = Cycle number (continuous, starts at 0.0)
   - `r` = Base amplification rate = `1.15`
   - `K` = Carrying capacity = `1.0e9`

   Use the **Euler Method** for numerical integration with a step size of `delta_c = 0.01`.
   Simulate up to `c = 40.0`.
   Find the exact continuous cycle `c` (to the nearest `0.01`) at the end of the step where the amplicon count `A` *first* exceeds or equals `1.0e7` (the threshold).

4. **Output Logging:**
   Write your final C++ program to `/home/user/pcr_pipeline.cpp`.
   Compile it using `g++` (e.g., `g++ -O2 -o pcr_pipeline pcr_pipeline.cpp`).
   Run it and write the results to `/home/user/simulation_results.txt` in the exact following format:
   ```
   Forward: [Forward Primer Sequence]
   Reverse: [Reverse Primer Sequence]
   Cq: [Cycle 'c' formatted to 2 decimal places where A >= 10^7]
   ```

Note: Ensure your C++ program handles standard fasta parsing (ignoring header lines starting with `>`). All sequences will only contain A, C, G, T.