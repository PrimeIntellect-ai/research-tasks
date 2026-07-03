You are a Machine Learning Engineer preparing synthetic training data for a robust anomaly detection system. Your task is to profile and compare the theoretical distributions of "normal" and "anomalous" sensor readings before generating the dataset.

Write a Bash script at `/home/user/prepare_data.sh` that orchestrates this mathematical profiling. You may use Python, `awk`, or `bc` within your Bash script to perform the calculations, but the entry point must be the Bash script itself.

The "normal" sensor readings follow a continuous distribution $A$ proportional to:
$f(x) = x^3 \cos^2(x/2)$ for $x \in [0, 2]$

The "anomalous" readings follow a Uniform distribution $B$ over the same interval $[0, 2]$.

Your script must perform the following steps:

1. **Numerical Integration (Normalization):**
   Calculate the normalization constant $Z$ for distribution $A$ over the interval $[0, 2]$. You must use the **Trapezoidal Rule** with exactly $N=1000$ equal-width steps ($\Delta x = 0.002$). 
   Save the calculated $Z$ value, rounded to exactly 4 decimal places, to `/home/user/norm_constant.txt`.

2. **Binning and Probability Calculation:**
   Divide the interval $[0, 2]$ into 10 equal-width bins: $[0.0, 0.2), [0.2, 0.4), \ldots, [1.8, 2.0]$.
   For each bin, calculate the theoretical probability mass for distribution $A$, $P_A(i)$, by integrating $f(x)/Z$ over the bin's range. Use the Trapezoidal Rule with exactly 100 equal-width steps per bin.
   Calculate the probability mass for distribution $B$, $P_B(i)$, for each bin.

3. **Probability Distribution Distance:**
   Calculate the Total Variation Distance (TVD) between the two binned (discrete) distributions $P_A$ and $P_B$. 
   Recall that for discrete distributions, $TVD = \frac{1}{2} \sum_{i=1}^{k} |P_A(i) - P_B(i)|$.
   Save the calculated TVD, rounded to exactly 4 decimal places, to `/home/user/tvd.txt`.

Make sure your script executes successfully when run as `bash /home/user/prepare_data.sh` and produces the two output files.