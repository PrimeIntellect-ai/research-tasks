You are an AI assistant helping a bioinformatics analyst process DNA sequences. 

Your task is to write and execute a C++ program that performs a statistical analysis on two sets of DNA sequences. 

You need to do the following:
1. Two files containing DNA sequences (one sequence per line) have been provided at `/home/user/seqA.txt` and `/home/user/seqB.txt`.
2. Write a C++ program at `/home/user/analyze.cpp` that reads both files and calculates the GC content (the proportion of 'G' and 'C' characters) for each sequence.
3. Calculate the sample mean and sample variance (using N-1 as the denominator) of the GC content for group A and group B.
4. Perform a Welch's t-test comparing the GC content of group A and group B. Calculate the t-statistic using the formula for unequal variances (use the order: Mean A - Mean B in the numerator).
5. In sequence evolution, the Jukes-Cantor distance $d$ relates to the proportion of different sites $p$ via the non-linear equation: 
   $d = -\frac{3}{4} \ln(1 - \frac{4}{3}p)$
   Compute the distance $d$ as the absolute difference between the mean GC content of group A and group B ($d = |\text{Mean A} - \text{Mean B}|$). Then, analytically or numerically solve the Jukes-Cantor equation for $p$.
6. Compile and run your C++ program.
7. Your program must output the results to `/home/user/results.txt` with exactly the following format (rounding values to 4 decimal places):

```
t_stat: [calculated t-statistic]
jc_p: [calculated p value]
```

Ensure your code compiles cleanly using standard C++17 (e.g., `g++ -std=c++17 /home/user/analyze.cpp -o /home/user/analyze`) and properly writes the output file.