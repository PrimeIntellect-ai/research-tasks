You are a performance engineer analyzing a legacy numerical computation pipeline that processes sensor calibration matrices. The system is crashing due to a matrix factorization step that fails on near-singular inputs. Because this is an embedded system build process, the pipeline must rely entirely on Bash, `awk`, and standard POSIX utilities (no Python, R, or compiled C allowed).

Your task is to write a bash script `/home/user/analyze_matrices.sh` that analyzes a dataset of 2x2 matrices to identify numerical stability issues, compute their inverses, validate the results, and generate a profiling report.

The input file will be located at `/home/user/input/matrices.csv` (which you should assume exists). It has no header, and each line is formatted as:
`id,a,b,c,d`
representing the 2x2 matrix:
[a, b]
[c, d]

Your script must do the following for each row:
1. **Compute Determinant:** Calculate $\Delta = ad - bc$.
2. **Stability Test:** If $|\Delta| < 10^{-6}$, classify the matrix as `UNSTABLE`.
3. **Inversion & Analytical Validation:** If the matrix is not `UNSTABLE` (i.e., it is `STABLE`), compute its inverse $A^{-1} = \frac{1}{\Delta} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix}$. 
   Then, compute the product $P = A \times A^{-1}$ and calculate the maximum absolute error between $P$ and the Identity matrix $I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$. 
   The max error is $\max(|P_{11}-1|, |P_{12}-0|, |P_{21}-0|, |P_{22}-1|)$.
4. **Accuracy Check:** If the max error is $> 10^{-9}$, classify it as `STABLE_INACCURATE`. Otherwise, classify it as `STABLE_ACCURATE`.

When executed, your script `/home/user/analyze_matrices.sh` must process the CSV and generate a report at `/home/user/report.txt` with exactly the following format:
```
Total Matrices: <total>
Unstable: <count>
Stable Accurate: <count>
Stable Inaccurate: <count>
```

Ensure your script has executable permissions (`chmod +x`). All calculations should be done in double precision (which is the default for `awk`).

Constraints:
- Only Bash, Awk, and standard POSIX coreutils are permitted.
- Write robust code that handles floating-point math securely using `awk` or `bc`.