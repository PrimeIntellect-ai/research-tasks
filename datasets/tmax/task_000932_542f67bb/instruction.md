You are a bioinformatics analyst tasked with modeling a viral infection and designing a diagnostic primer.

Your task is to create a Jupyter notebook at `/home/user/analysis.ipynb` that performs the following two steps, and then execute it headlessly via the command line to generate the results.

**Step 1: Viral Population Modeling (ODE)**
Model the viral load $V(t)$ using the following modified logistic growth differential equation:
$dV/dt = r \cdot V \cdot (1 - V/K) - d \cdot V$
Where:
- $r = 0.5$ (replication rate)
- $K = 1000$ (carrying capacity)
- $d = 0.1$ (clearance rate)

Given the initial condition $V(0) = 10$, use `scipy.integrate.solve_ivp` (with the default RK45 method) to solve the system from $t=0$ to $t=100$. Extract the final viral load at $t=100$.

**Step 2: Primer Design**
You need to find a suitable 8-bp primer from the following viral sequence:
`"ATGGCCGCCATATTGAGCGGCCGCATTAG"`

Write a sliding window algorithm to find the 8-base-pair contiguous subsequence with the highest GC-content (number of 'G' and 'C' nucleotides). If there is a tie for the highest GC-content, select the first one that appears in the sequence (reading left to right).

**Step 3: Notebook Orchestration & Output**
The notebook must write a JSON file to `/home/user/results.json` containing the exact keys:
- `"final_V"`: The viral load at $t=100$, rounded to 2 decimal places (float).
- `"best_primer"`: The 8-bp primer sequence you identified (string).

Once you have written `/home/user/analysis.ipynb`, install any necessary packages and use `jupyter nbconvert` to execute the notebook headlessly. Save the executed notebook as `/home/user/analysis_out.ipynb`. 

Ensure that after your steps are complete, `/home/user/results.json` and `/home/user/analysis_out.ipynb` exist and contain the correct results.