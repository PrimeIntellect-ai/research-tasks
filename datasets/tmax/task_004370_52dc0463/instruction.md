You are assisting a researcher who is running particle simulations. They have an experimental reference dataset of particle energies and need to compare it against a simulated distribution.

Your task is to write a C program `/home/user/simulate.c` that generates the simulated data, estimates the probability density functions of both datasets using histograms, and computes the Bhattacharyya distance between them.

Here are the exact requirements:

1. **Reference Data**: Read the reference dataset from `/home/user/reference.txt`. It contains 10,000 floating-point numbers, one per line.

2. **Simulated Data**: Generate exactly 10,000 simulated particle energies from a Normal distribution $N(\mu=5.0, \sigma=2.0)$ using the Box-Muller transform. 
To ensure cross-platform determinism, implement the following Linear Congruential Generator (LCG) instead of using `rand()`:
```c
unsigned int state = 42;
unsigned int next_rand() {
    state = (state * 1103515245 + 12345) % 2147483648;
    return state;
}
```
For each of the 10,000 particles, generate two uniform random variables $u_1$ and $u_2$ as follows:
```c
double u1 = (next_rand() + 1.0) / 2147483649.0;
double u2 = (next_rand() + 1.0) / 2147483649.0;
```
Calculate the standard normal variable $z$:
$z = \sqrt{-2.0 \cdot \ln(u_1)} \cdot \cos(2.0 \cdot \pi \cdot u_2)$
And the particle energy: $E = 5.0 + 2.0 \cdot z$

3. **Density Estimation (Histograms)**:
Compute a histogram for both the reference data and the simulated data.
- Range: `[0.0, 10.0)`
- Number of bins: 100 (each of width 0.1)
- Values $< 0.0$ or $\ge 10.0$ should be strictly ignored. They do not count toward the bin counts, nor the total count of valid points used for normalization.
- A value `x` falls into bin index `i = (int)(x / 0.1)`.
- Convert the bin counts into valid probability distributions $P$ (reference) and $Q$ (simulated) by dividing each bin's count by the total number of valid points in its respective dataset.

4. **Bhattacharyya Distance**:
Calculate the Bhattacharyya distance between $P$ and $Q$:
$D_B = -\ln \left( \sum_{i=0}^{99} \sqrt{P_i \cdot Q_i} \right)$

5. **Output**:
Write the final distance as a floating-point number formatted to 4 decimal places (e.g., `0.0123`) to the file `/home/user/distance.txt`.

Compile and run your code to produce `/home/user/distance.txt`. Standard math libraries (`-lm`) are available and required.