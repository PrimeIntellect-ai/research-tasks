You are a performance engineer tasked with profiling and stabilizing a legacy scientific computing pipeline. 

We have a proprietary spectral deconvolution tool located at `/app/bin/spec_deconv`. It is a stripped, UPX-packed Linux binary. It takes a time-domain signal (a single-column text file of floating-point numbers) as input and solves a nonlinear system to extract spectral peaks. 

Recently, we discovered that certain signals cause the solver to diverge, leading to an infinite loop and 100% CPU lockup. You need to write a Bash-based sanitization wrapper that analyzes the input signal before passing it to the binary. 

Your objective:
1. Create a reproducible scientific environment (you may install tools like `python3-numpy`, `octave`, `jq`, or standard math libraries using `apt` or `pip`).
2. Analyze the behavior of `/app/bin/spec_deconv` against the provided datasets.
3. Write a Bash script at `/home/user/sanitize_wrapper.sh` that takes exactly one argument (the input signal file path).
4. The script must output exactly `REJECT` to stdout and exit with code 1 if the signal contains the mathematical properties that cause the binary to hang.
5. The script must pass the file to `/app/bin/spec_deconv`, print its stdout, and exit with code 0 if the signal is safe.

Data provided:
- A directory of known "safe" signals: `/app/corpus/clean/`
- A directory of known "divergent" signals: `/app/corpus/evil/`

Your wrapper will be evaluated automatically. It must successfully preserve 100% of the clean corpus and reject 100% of the evil corpus without hanging.