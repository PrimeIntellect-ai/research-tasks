As a researcher in computational statistics, you need to analyze the approximation quality of using a Student's t-distribution to model standard normally distributed data as the degrees of freedom ($\nu$) vary. 

Your task is to write a C++ program from scratch that computes the Kullback-Leibler (KL) divergence from a standard Normal distribution $P$ to a Student's t-distribution $Q_\nu$, as well as the sensitivity (derivative) of this divergence with respect to $\nu$.

Write your code in `/home/user/kl_div.cpp` and implement the following requirements:

1. **Probability Density Functions**:
   - $P(x)$: Standard Normal PDF.
   - $Q(x, \nu)$: Student's t-distribution PDF with $\nu$ degrees of freedom. (Use `std::tgamma` from `<cmath>`).

2. **Numerical Integration**:
   - Compute the KL divergence $D_{KL}(P || Q_\nu) = \int_{-20}^{20} P(x) \log\left(\frac{P(x) + 10^{-15}}{Q(x, \nu) + 10^{-15}}\right) dx$.
   - Note the $10^{-15}$ terms added to both numerator and denominator for **numerical stability**.
   - Use the **composite Simpson's 1/3 rule** with exactly $N = 100,000$ intervals (i.e., $100,001$ evaluation points) over the range $[-20, 20]$.

3. **Numerical Differentiation**:
   - Compute the derivative $\frac{d}{d\nu} D_{KL}(P || Q_\nu)$ at $\nu = 3.0$.
   - Use the **central difference method** with a step size of $h = 0.01$ (i.e., evaluate at $\nu = 3.01$ and $\nu = 2.99$).

4. **Compilation and Output**:
   - Compile your program to an executable at `/home/user/kl_calc` using the command: `g++ -O3 -std=c++11 /home/user/kl_div.cpp -o /home/user/kl_calc`.
   - Run the executable. It must output exactly two lines to a file `/home/user/results.txt`.
   - The first line must be the computed KL divergence at $\nu = 3.0$.
   - The second line must be the numerical derivative at $\nu = 3.0$.
   - Both values must be formatted to exactly **6 decimal places**.

Ensure your math and Simpson's rule implementations are precise. You only need standard C++ libraries (`<iostream>`, `<cmath>`, `<fstream>`, `<iomanip>`, etc.).