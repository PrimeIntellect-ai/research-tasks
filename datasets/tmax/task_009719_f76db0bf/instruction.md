You are a performance engineer tasked with optimizing a slow bioinformatics prototype. The application aligns primer sequences against target DNA and then solves a binding kinetics model. You need to rewrite the core logic in Rust to prove the performance gains.

The data for this task is provided below:

Target Sequence (`/home/user/target.txt`):
`CGATCGTAGCTAGCTAGCATCGTAGCTAG`

Primer Sequence (`/home/user/primer.txt`):
`GTAGCTA`

Substitution Matrix (`/home/user/matrix.txt`):
```
  A  C  G  T
A 5 -1 -2 -1
C -1 5 -1 -2
G -2 -1 5 -1
T -1 -2 -1 5
```
Rows and columns correspond to 'A', 'C', 'G', 'T' in that exact order.

**Your Objective:**
Write and execute a Rust program (save it as `/home/user/optimizer.rs`) that does the following:
1. **Multi-dimensional array manipulation & Sequence alignment:** 
   Read the substitution matrix into a 2D array/matrix structure. Slide the primer sequence across the target sequence one position at a time (gapless alignment). For each window, compute the alignment score by summing the substitution matrix values for each aligned pair of bases. 
   Find the maximum alignment score, $S$.
2. **Nonlinear equation solving:**
   Use the maximum score $S$ to solve the following nonlinear binding equation for $x$ (where $x > 0$):
   $e^x + S \cdot x - 200 = 0$
   Implement a numerical solver (like Newton-Raphson or bisection) in your Rust code to find the root $x$ accurate to at least 4 decimal places.
3. **Output:**
   Your Rust program should write the result to a file located at `/home/user/result.txt` in the following exact format:
   ```
   Max Score: [S]
   Root: [x rounded to 4 decimal places]
   ```

Write, compile, and run your Rust code to produce `/home/user/result.txt`.