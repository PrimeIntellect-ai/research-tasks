You are an AI assistant helping a machine learning engineer prepare spatial training data for a microfluidic PCR (Polymerase Chain Reaction) chip model.

We need to build a C-based data preparation pipeline that maps DNA primers to their optimal spatial location on the chip based on temperature zones, and then evaluates a linear regression hypothesis on the results.

You are provided with a file containing DNA primer sequences at `/home/user/primers.txt` (one sequence per line, uppercase A, T, C, G).

Write a C program (e.g., at `/home/user/prepare_data.c`) and compile/run it to perform the following steps:

1. **Mesh Refinement & Domain Decomposition**: 
   The microfluidic chip has a 1D spatial domain $x \in [0, 10]$ mm. The heater is at the center ($x=5$). Create a non-uniform mesh of 101 points (index $i = 0, 1, \dots, 100$) strongly refined near the center. 
   Calculate the coordinates $x_i$ using the formula:
   $z_i = \frac{i - 50}{50.0}$
   $x_i = 5.0 + 5.0 \times \text{sgn}(z_i) \times z_i^2$
   where $\text{sgn}(z)$ is 1 if $z > 0$, -1 if $z < 0$, and 0 if $z = 0$.

2. **Temperature Profile**:
   Calculate the steady-state temperature $T(x_i)$ at each mesh node:
   $T(x_i) = 40.0 + 50.0 \times \exp\left(-0.5 \times (x_i - 5.0)^2\right)$

3. **Primer Analysis**:
   For each sequence in `/home/user/primers.txt`, calculate its GC-content fraction:
   $f_{GC} = \frac{\text{Count of G and C}}{\text{Total Sequence Length}}$
   Then, estimate its melting temperature using a simplified linear model:
   $T_m = 50.0 + 40.0 \times f_{GC}$

4. **Spatial Alignment**:
   For each primer, find the mesh index $i^*$ that minimizes the absolute difference $|T(x_i) - T_m|$. The optimal location for this primer is $x_{i^*}$. (If there is a tie, pick the lowest index $i^*$).

5. **Data Output**:
   Write the processed data to `/home/user/training_data.csv` with the exact header:
   `Sequence,f_GC,Tm,Optimal_X`
   Print the float values to exactly 4 decimal places (e.g., `%.4f`).

6. **Curve Fitting & Statistical Hypothesis**:
   We want to test the hypothesis that the optimal spatial location is linearly dependent on the GC content. Perform an Ordinary Least Squares (OLS) linear regression of `Optimal_X` ($y$) on `f_GC` ($x$).
   Calculate:
   - The regression slope ($m$)
   - The intercept ($c$)
   - The Residual Sum of Squares (RSS) for this linear hypothesis: $\text{RSS} = \sum (y_k - (m \cdot x_k + c))^2$
   
   Output these three values, separated by commas, to exactly 4 decimal places in a file named `/home/user/stats.log` (format: `slope,intercept,RSS`).

**Constraints**:
- You must write and execute the C code to accomplish this. You may use standard C libraries (`stdio.h`, `math.h`, `string.h`, `stdlib.h`).
- Link the math library when compiling (`-lm`).