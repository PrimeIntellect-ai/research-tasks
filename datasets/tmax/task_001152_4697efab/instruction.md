You are a bioinformatics analyst tasked with simulating the population dynamics of various bacterial strains based on their genetic signatures.

Your task is to create a reproducible computational pipeline in Go that parses a FASTA file, uses the sequence data to parameterize an Ordinary Differential Equation (ODE), solves it numerically, and includes a regression test.

Here are the requirements:

1. **Setup Workspace**: Create a directory `/home/user/bio_sim` and initialize a Go module named `bio_sim`.

2. **Input Data**: A FASTA file is located at `/home/user/input.fasta` (you will need to assume it exists when your program runs, but for testing, you can create a dummy one). The FASTA format contains sequences with headers starting with `>`.

3. **ODE Simulation (Logistic Growth)**:
   For each sequence in the FASTA file, calculate its specific growth rate $r$, defined exactly as the GC-content of the sequence (i.e., the total number of 'G' and 'C' characters divided by the total length of the sequence, ignoring case and whitespace).
   
   Using this growth rate $r$, simulate the population $P(t)$ of the strain using the logistic growth ODE:
   $dP/dt = r \cdot P \cdot (1 - P / K)$
   
   Where:
   - Carrying capacity $K = 1000.0$
   - Initial population $P(0) = 10.0$
   
   Solve this ODE using the explicit **Euler method** from $t = 0$ to $t = 10$ with a time step of $dt = 0.1$ (exactly 100 steps). Use `float64` for all calculations.

4. **Output Generation**:
   Your Go program `main.go` must read `/home/user/input.fasta` and write the results to a CSV file at `/home/user/results.csv`.
   The CSV must have the header `StrainID,FinalPopulation`.
   `StrainID` is the sequence header (excluding the `>` and any leading/trailing whitespace).
   `FinalPopulation` is the value of $P(10)$ formatted to exactly 2 decimal places.

5. **Regression Testing**:
   Write a Go test file `main_test.go` that contains a regression test. It must test the ODE solver logic with a mock sequence that has exactly 50% GC content ($r = 0.5$). The test should verify that after 100 steps of $dt = 0.1$, the final population $P(10)$ equals `1094.02` (allowing for a small floating-point tolerance of $\pm 0.1$). If it fails, the test must use `t.Errorf`.

Ensure your code is clean and that `go build`, `go test`, and `go run main.go` execute successfully in `/home/user/bio_sim`.