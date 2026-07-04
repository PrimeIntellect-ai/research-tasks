You are a performance engineer profiling the output of a parallel Monte Carlo simulation. The simulations emit binary trace files containing arrays of `float64` values. We have a local vendored Go package called `mcparser` that reads these trace files, but it currently fails to compile due to a recent bad commit.

Additionally, our simulation occasionally suffers from anomalous high-frequency noise injection due to thread-synchronization glitches. We need a detector to filter out these "evil" anomalous traces from the "clean" ones.

Your task:
1. **Fix the vendored package**: The `mcparser` package is vendored at `/app/mcparser`. Identify and fix the bug preventing it from compiling.
2. **Write a classifier**: Create a Go program at `/home/user/detect.go`. It must accept a single command-line argument (the path to a trace file), use `mcparser.Parse(filepath)` to load the `[]float64` data, and classify the trace.
3. **Classification Logic**: Since you cannot download external FFT libraries (no internet access is available for dependencies), you must use a time-domain proxy for high-frequency spectral analysis: the "Roughness" metric. 
   Calculate the average squared difference between consecutive points: `R = (1 / (N-1)) * sum((x[i] - x[i-1])^2)`.
   * "Clean" Monte Carlo traces have a smooth distribution where `R < 2.0`.
   * "Evil" traces have high-frequency noise injected, resulting in `R > 5.0`.
4. **Output format**: Your script must print exactly `CLEAN` to standard output if the trace is clean, and exactly `EVIL` if the trace contains high-frequency anomalies. It should exit with code 0 in both successful classification cases.

You can test your classifier against the offline corpora provided at `/app/corpus/clean` and `/app/corpus/evil`. A successful solution will correctly classify 100% of both sets.