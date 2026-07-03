As a machine learning engineer, you need to prepare a synthetic dataset of spectral features for training an anomaly detection model. You must write a C program that uses Monte Carlo simulation to generate noisy signals, processes them using Fourier transforms, and extracts statistical features via linear regression. 

Please perform the following steps:
1. Install the `libfftw3-dev` package since you will need the FFTW3 library.
2. Write a C program located at `/home/user/generate_data.c`. 
3. The program must implement a reproducible pipeline (using a custom pseudo-random number generator provided below to ensure cross-platform consistency).
4. For `ID` from 0 to 99 (100 signals total):
    * Generate a signal of $N=100$ points, representing 1 second of data sampled at 100 Hz ($t = 0.00, 0.01, ..., 0.99$).
    * The base signal is a 5 Hz sine wave: $y(t) = \sin(2 \pi \cdot 5 \cdot t)$.
    * Generate a random noise amplitude $A$ for this signal: $A = 0.1 + 1.9 \cdot \text{next\_rand}()$.
    * For each point $t$, add uniform noise $v \in [-A, A]$ to $y(t)$. Generate $v$ as $v = -A + 2A \cdot \text{next\_rand}()$.
    * Note: Generate $A$ first, then generate $v$ for $t=0$, then $v$ for $t=0.01$, etc.
5. Compute the 1D real-to-complex Fast Fourier Transform (FFT) of the 100-point signal using `fftw_plan_dft_r2c_1d`.
6. Calculate the amplitude spectrum $M[k] = \sqrt{Re[k]^2 + Im[k]^2}$ for the frequency bins $k \in [10, 40]$ (which correspond to 10 Hz to 40 Hz).
7. Perform a simple linear regression (Ordinary Least Squares) on these specific bins to fit $M[k] = m \cdot k + c$. Calculate the slope $m$.
8. Append the result to `/home/user/training_metadata.csv` in the format: `ID,A,Slope`. Format floats to exactly 4 decimal places (e.g., `0,1.2345,-0.0012`). Do not include a header row.

Here is the exact PRNG you must use to ensure reproducible outputs. Seed it with `state = 42` at the very beginning of your `main` function:
```c
#include <stdint.h>
uint32_t state = 42;
double next_rand() {
    state = (state * 1103515245 + 12345) % 2147483648;
    return (double)state / 2147483648.0;
}
```

Compile your code using `gcc /home/user/generate_data.c -o /home/user/generate_data -lfftw3 -lm` and run it to produce the CSV file.