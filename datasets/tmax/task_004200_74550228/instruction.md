You are a performance engineer tasked with profiling and optimizing a numerical solver used in acoustic propagation modeling.

Your task consists of the following steps:

1. **Audio Decoding and Compilation:** 
   We have a proprietary audio signal containing the key acoustic parameter, `K`, embedded as a spoken value. The source code for our internal audio decoder is located at `/app/decoder_src/`.
   - Compile the audio decoder from source. The directory contains a `Makefile`.
   - Run the compiled binary on the audio fixture `/app/signal.wav` to extract the spoken parameter `K`.

2. **Numerical Equation Solving:**
   The core acoustic propagation is modeled by finding the root of the nonlinear equation:
   `f(x) = x^3 - K * x + 1 = 0`
   
   You need to implement a solver using the Newton-Raphson method strictly using Bash, `awk`, and standard Linux coreutils. No Python, Perl, or compiled C++ allowed for the solver itself.
   
   - You are provided with a file `/app/guesses.txt` containing 1000 initial guesses (one float per line).
   - Write an optimized `awk` or Bash script that reads each initial guess, performs Newton-Raphson iterations until convergence (tolerance of 1e-7) or maximum 100 iterations, and calculates the root.
   - For numerical stability, if the derivative becomes exactly zero, your script should output `NaN` for that guess.
   
3. **Execution and Output:**
   - Process all 1000 guesses.
   - Save the final computed roots to `/home/user/roots.txt` (one root per line, corresponding to the order of inputs).

Your final script must be highly performant (e.g., capable of processing all 1000 inputs in under a second). The automated verifier will evaluate the accuracy of your roots against a high-precision reference solver.