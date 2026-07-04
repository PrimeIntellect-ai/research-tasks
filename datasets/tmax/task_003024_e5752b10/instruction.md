You are a data scientist working on a machine learning pipeline written in C. We are trying to process streaming sensor data, but we keep running into a "data leakage" problem where statistics from our test set are leaking into the training normalizer. 

To solve this, we need to enforce a strict separation between fitting (updating statistics) and transforming (scaling data).

We have vendored a streaming statistics library called `libwelford-1.0.0` located at `/app/libwelford-1.0.0`. It calculates streaming means and variances using Welford's numerical accuracy algorithm to prevent catastrophic cancellation.

However, the pipeline is currently broken:
1. The library's `Makefile` has a bug and fails to build the static archive `libwelford.a`. You must fix the `Makefile` and build the library.
2. You need to write a C program that uses this library to enforce a strict `fit_transform` schema without leaking future data into past transformations.

Write your program in `/home/user/streaming_scaler.c` and compile it to `/home/user/streaming_scaler`. It must link against the fixed `/app/libwelford-1.0.0/libwelford.a` and include `-lm`.

**Program Specifications (`/home/user/streaming_scaler`):**
- Read lines from `stdin` until EOF. Maximum line length is 64 bytes.
- Initialize a single `WelfordState` at the start of the program.
- Each line will strictly be in one of two formats: `FIT <float>` or `TRANSFORM <float>`.
- If the line is `FIT <float>`:
  - Update the Welford state with the given float value.
  - Print exactly `FIT_OK\n` to `stdout`.
- If the line is `TRANSFORM <float>`:
  - Compute the Z-score normalization of the float using the *current* mean and variance of the Welford state. Formula: `(val - mean) / sqrt(variance)`.
  - Print the scaled value to `stdout` formatted as `%.6f\n`.
  - If the current variance is exactly `0.0`, print `0.000000\n`.
- Ignore any empty lines or improperly formatted lines (do not print anything for them).

The header `/app/libwelford-1.0.0/welford.h` contains:
```c
typedef struct {
    int count;
    double mean;
    double m2;
} WelfordState;

void welford_init(WelfordState* state);
void welford_update(WelfordState* state, double val);
double welford_mean(const WelfordState* state);
double welford_variance(const WelfordState* state); // Returns m2/count, or 0.0 if count < 2
```

Compile the final executable correctly. Your output must strictly match the oracle behavior across arbitrary streams of input to ensure no data leaks happen during online cross-validation.