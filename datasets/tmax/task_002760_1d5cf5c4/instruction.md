I'm working on cleaning up a noisy dataset of sensor readings using a Bayesian inference approach (specifically, a 1D Kalman Filter). 

I have a dataset located at `/home/user/noisy_sensor.txt` containing 1000 noisy floating-point readings (one per line). 

I downloaded a tiny, open-source C library for this called `kalman-c` version 1.0. The source code is vendored at `/app/kalman-c-1.0/`. However, it currently fails to compile because of a numerical library configuration error in its `Makefile` (it fails to link the standard math library).

Please do the following:
1. Fix the `Makefile` in `/app/kalman-c-1.0/` and run `make` to compile the static library `libkalman.a`.
2. Write a C program at `/home/user/clean.c` that reads the noisy data from `/home/user/noisy_sensor.txt`.
3. Use the library's function `void kalman_filter(const double* input, double* output, int length, double process_variance, double measurement_variance);` defined in `kalman.h`. Configure the Bayesian model with a process variance (`q`) of `1e-4` and a measurement variance (`r`) of `0.02`.
4. Compile your program and link it against the `libkalman.a` library you built.
5. Execute your program and write the smoothed data to `/home/user/cleaned_sensor.txt`, with each value formatted to six decimal places (`%.6f`), one per line.

Ensure your cleaned dataset matches the expected probabilistic output closely. An automated test will evaluate the Mean Squared Error (MSE) of your output against a perfectly smoothed reference signal.