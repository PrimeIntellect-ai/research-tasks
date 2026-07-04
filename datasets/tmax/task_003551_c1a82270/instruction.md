As a data scientist cleaning and validating a dataset, you need to evaluate the stability of the dataset's mean using bootstrap sampling. The previous implementation used the standard C `rand()` function, which lacks the statistical rigor and numerical accuracy required for our analysis. 

Your task is to implement a robust bootstrapping tool in C using the GNU Scientific Library (GSL).

1. Install the necessary GSL development packages (`libgsl-dev`).
2. A dataset of 100 floating-point numbers is located at `/home/user/data.txt` (one number per line).
3. Create a C program at `/home/user/bootstrap.c` that does the following:
   - Reads the 100 numbers into an array.
   - Initializes the GSL Mersenne Twister random number generator (`gsl_rng_mt19937`) with the seed `42`.
   - Generates $B = 1000$ bootstrap samples. Each bootstrap sample should consist of $N = 100$ data points drawn **with replacement** from the original dataset. Use `gsl_rng_uniform_int(r, 100)` to pick the indices.
   - Calculates the mean for each of the 1000 bootstrap samples.
   - Calculates the overall mean of these 1000 bootstrap means, and the sample standard deviation of these 1000 means (using $B-1$ in the denominator).
4. Compile your program to `/home/user/bootstrap`. (Hint: you will need to link `gsl`, `gslcblas`, and `m`).
5. Run the compiled program and save the output to `/home/user/result.txt`. The output must be exactly two lines in the following format, with values printed to 6 decimal places:

```
Overall Mean: [value]
StdDev: [value]
```