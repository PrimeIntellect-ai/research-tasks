You are a bioinformatics analyst trying to identify coding regions in a DNA sequence using genomic signal processing. A known property of coding regions is the "period-3" periodicity, which can be detected using Fourier transforms.

Write a C++ program `/home/user/analyze.cpp` to calculate the spectral power at frequency $f = 1/3$ for a given DNA sequence.

1. Read the DNA sequence from `/home/user/dna.txt` (the file contains a single string of uppercase nucleotides on one line).
2. Map the nucleotides to numerical values: A=1, C=2, G=3, T=4. Let this be the sequence $x_n$ where $n$ is the 0-based index.
3. Compute the Fourier components at $f = 1/3$:
   $X = \sum_{n=0}^{N-1} x_n \cos(2 \pi n / 3)$
   $Y = \sum_{n=0}^{N-1} x_n \sin(2 \pi n / 3)$
4. Calculate the Power: $P = X^2 + Y^2$.
5. Your program must output the final Power $P$, rounded to exactly two decimal places (e.g., `12.34`), and write this value to `/home/user/power.txt`.

Use standard bash commands and `g++` to compile and run your program. Do not use external libraries other than the C++ standard library (`<iostream>`, `<fstream>`, `<cmath>`, etc.).