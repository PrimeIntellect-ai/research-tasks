You are a bioinformatics data scientist trying to reproduce an older experiment. Your predecessor left behind an audio voice memo containing a critical DNA primer sequence, a reference genome dataset, and a C++ script used for fitting a non-linear biological model based on that primer's location.

Unfortunately, the C++ simulation produces non-reproducible, unstable results due to floating-point reduction order issues (it currently uses a naive parallel accumulation strategy that loses precision and lacks determinism).

Your objectives are:
1. **Transcribe Audio:** Listen to or process `/app/primer_memo.wav` to extract the spoken DNA primer sequence (it will be a short sequence of letters like A, C, G, T). You may use any available command-line tools to transcribe it.
2. **Primer Alignment:** Find the exact 0-indexed starting position of this primer sequence within the reference genome located at `/app/reference.fasta`. Let this position be `P`.
3. **Fix the Model Fitter:** Examine `/home/user/fitter.cpp`. It fits a non-linear equation to a large dataset `/app/measurements.csv` using gradient descent. The initial parameter for the phase shift in the model must be set to the position `P` you found.
4. **Numerical Stability:** The current implementation in `fitter.cpp` uses single-precision floats and a naive parallel reduction loop for computing the Mean Squared Error loss and gradients. This causes the final fitted weights to be wildly unstable across different runs. Refactor the C++ code to guarantee strict numerical determinism and high precision (e.g., by using `double` precision and implementing Kahan summation for the gradient/loss accumulations, or by strictly ordering the reduction).
5. **Output:** Compile your fixed C++ program and run it. The program must output the final fitted parameters (comma-separated, e.g., `theta0, theta1, theta2`) to a file strictly located at `/home/user/model_weights.txt`.

Your final model weights will be evaluated against a golden reference implementation. Your weights must be numerically stable (variance of 0 across multiple runs) and achieve a parameter L2 error of less than 1e-4 compared to the true optimum.