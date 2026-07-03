A former researcher in our lab left behind a compiled binary, `/app/spectro_sim`, which simulates the vibrational spectroscopy of molecular networks. It takes a molecule's mass and bond properties and outputs the spectral frequencies. Unfortunately, the source code is lost, the binary is stripped, and it is notoriously slow. It also occasionally suffers from slight floating-point non-determinism.

We need a clean, fast, and stable replacement implementation. Your task is to analyze the behavior of `/app/spectro_sim` by treating it as an oracle, deduce the underlying mathematical model it computes, and implement a faster replacement in Python.

**Input format for both the binary and your script:**
A text file where:
- The first line contains an integer `N` (number of atoms/nodes, $2 \le N \le 100$).
- The second line contains `N` space-separated floating-point numbers representing the mass of each atom.
- The next `N` lines contain an `N x N` symmetric matrix of floating-point numbers representing the bond spring constants (adjacency matrix). A value of 0 means no bond.

**Output format:**
The program must output `N` space-separated floating-point numbers on a single line, representing the sorted spectral frequencies from lowest to highest. 

**Requirements:**
1. Investigate `/app/spectro_sim` (you can pass an input file path as its first argument) to deduce the physics model. (Hint: It involves graph Laplacians, linear/nonlinear equation solving for eigenvalues, and mass matrices).
2. Write a Python script at `/home/user/fast_sim.py` that takes the input file path as its first command-line argument and prints the resulting frequencies to standard output.
3. Your script must be significantly faster than the binary and numerically stable.

Your solution will be evaluated on a hidden dataset of 50 molecular graphs. Your output must match the binary's output (within a small tolerance) but be at least 10x faster.