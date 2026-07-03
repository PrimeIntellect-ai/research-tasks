You are a bioinformatics analyst tasked with evaluating a set of newly sequenced genetic fragments. 

Your objective is to write a C++ program `/home/user/analyze_gc.cpp` that processes a FASTA file located at `/home/user/sequences.fasta`. The program must perform the following steps:

1. **FASTA Parsing & Data Extraction**: Parse the FASTA file. For each sequence, calculate the GC-ratio. The GC-ratio is defined as the number of 'G' and 'C' characters divided by the total number of sequence characters (ignoring newline characters and the header lines starting with `>`).
2. **Data Reshaping**: Sort the computed GC-ratios in ascending order: $r_0 \le r_1 \le \dots \le r_{N-1}$, where $N$ is the total number of sequences.
3. **Numerical Integration**: Treat these sorted ratios as discrete samples of a function over the normalized domain $[0, 1]$. The $x$-coordinates are evenly spaced: $x_i = \frac{i}{N-1}$ for $i = 0, \dots, N-1$. Calculate the area under this curve using the **Trapezoidal Rule**.
4. **Statistical Hypothesis Comparison**: 
   - Calculate the sample mean ($\mu$) of the GC-ratios.
   - Calculate the standard deviation ($\sigma$) of the GC-ratios. Use $N$ in the denominator (i.e., population standard deviation of the sample, $\sigma = \sqrt{\frac{1}{N} \sum (r_i - \mu)^2}$).
   - Calculate the Z-statistic to test the null hypothesis that the true mean GC-ratio is $0.5$. The formula is $Z = \frac{\mu - 0.5}{\sigma / \sqrt{N}}$.
   
5. **Output**: Your C++ program must write the computed values to a file named `/home/user/stats.txt`. The output must be formatted exactly as follows, with floating-point values rounded to exactly 4 decimal places:
```
Integral: 0.xxxx
Mean: 0.xxxx
Z-stat: 0.xxxx
```

Compile and run your C++ program to generate the `/home/user/stats.txt` file. You may use standard C++11 (or later) libraries. No external libraries are required or permitted.