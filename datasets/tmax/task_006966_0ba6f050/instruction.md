You are helping a data scientist set up a baseline regression test for a new C-based bioinformatics modeling pipeline. 

We need to extract sequence lengths from a FASTA file and use them as initial conditions for a simple numerical ODE solver. 

Write a C program located at `/home/user/solve_model.c` that does the following:
1. Parses the FASTA file located at `/home/user/input.fasta`.
2. For each sequence, extracts the sequence ID (everything after `>` up to the first space or newline) and calculates the total length $L$ of the sequence (number of standard characters, ignoring newlines).
3. Uses $L$ as the initial condition $y(0) = L$ for a numerical ODE simulation.
4. Solves the decay ODE $dy/dt = -0.1 \cdot y$ using the **Euler method** with a step size of $dt = 0.5$ from $t = 0$ to $t = 5.0$ (exactly 10 steps). 
5. Writes the final $y(5.0)$ value for each sequence to a CSV file at `/home/user/results.csv`. 

The output format in `/home/user/results.csv` must be exactly:
```
SequenceID,FinalY
```
Where `FinalY` is printed as a floating point number rounded to exactly 2 decimal places (e.g., `%.2f`). 

Compile your C program into an executable named `/home/user/solve_model` and run it to produce the `results.csv` file.