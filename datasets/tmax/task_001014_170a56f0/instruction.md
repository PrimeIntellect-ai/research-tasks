You are a data scientist analyzing wastewater sequencing data to track a viral variant's population dynamics. 

Your task is to write a C++ program that processes daily DNA sequences, counts the occurrences of a specific variant, fits a population dynamics ODE model to this data, and then creates a visualization.

Here are the detailed steps and requirements:

**1. Sequence Alignment & Counting:**
You have 10 FASTA files located in `/home/user/data/` named `day_1.fasta` through `day_10.fasta`. 
The signature sequence (primer) for the variant we are tracking is: `ATGCGTACGTAGCTA`.
Your C++ program (`/home/user/variant_fitter.cpp`) must read these files and count how many sequences in each file contain the signature sequence as a substring, allowing for **at most 1 mismatch** (substitution only, no insertions or deletions). Note: the signature sequence must be contiguous, but one character can be different.

**2. ODE Numerical Solving & Fitting:**
The growth of the variant follows the logistic growth ODE:
`dV/dt = r * V * (1 - V / K)`
Where:
- `V` is the variant count on a given day.
- `t` is the time in days (Day 1 is t=0, Day 2 is t=1, ..., Day 10 is t=9).
- `K = 10000` (the carrying capacity).
- `r` is the unknown growth rate.

You must fit this model to your daily counts.
- Set `V(0)` exactly equal to the actual count on Day 1.
- Use the **Forward Euler method** to simulate the ODE from t=0 to t=9 using a time step of `dt = 0.1` days. 
- Perform a grid search to find the value of `r` in the range `[0.00, 1.00]` inclusive, with a step size of `0.01`, that minimizes the Mean Squared Error (MSE) between the actual daily counts (Days 1 to 10) and the ODE's predicted counts at those exact integer days (t=0, 1, ..., 9). If there is a tie, pick the smallest `r`.

**3. Output Generation:**
Your C++ program must output two files:
- `/home/user/r_value.txt`: containing only the single best `r` value formatted to two decimal places (e.g., `0.34`).
- `/home/user/results.csv`: a CSV file with a header `Day,Actual,Predicted` and 10 rows of data (for Day 1 to 10). The `Predicted` values should be printed to two decimal places.

**4. Experimental Data Visualization:**
Write a Python script `/home/user/plot.py` that reads `/home/user/results.csv` and generates a plot saved as `/home/user/fit_plot.png`. The plot must contain the actual counts as scatter points and the predicted counts as a line.

**Execution:**
Compile your C++ code using standard `g++` (`g++ -O3 variant_fitter.cpp -o variant_fitter`) and run it. Then run your Python script. Let me know when `/home/user/r_value.txt`, `/home/user/results.csv`, and `/home/user/fit_plot.png` are ready.