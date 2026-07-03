You are a performance engineer working on a bioinformatics pipeline. Your team has written a Go application that analyzes the thermodynamic properties and alignment score distributions of DNA primers. However, the application is currently running too slowly, and the statistical validation module is incomplete.

Your task involves compiling the sequence generator, completing the Go analysis code with numerical integration and CPU profiling, and then analyzing the bottleneck.

Here are your specific instructions:

1. **Compile the Sequence Generator:**
   In `/home/user/seqgen`, there is C source code for a primer generation tool. Compile it using the provided Makefile. Once compiled, run `./seqgen 10000 > /home/user/primers.fasta` to generate a deterministic dataset of 10,000 primer sequences.

2. **Complete the Go Application:**
   In `/home/user/analyzer/main.go`, you will find the Go application. You need to make three modifications:
   a) Implement the `SimpsonIntegration(x, y []float64) float64` function. The slices `x` and `y` represent points of a probability density function. Use Simpson's 1/3 rule to compute the numerical integral. You can assume the number of points is always odd (even number of intervals) and the `x` points are evenly spaced.
   b) Add CPU profiling to the application using the `runtime/pprof` standard library package. The profile must be written to `/home/user/cpu.prof` and capture the entire execution of the `main()` function after argument parsing.

3. **Run and Profile:**
   Build the Go application and run it against the generated sequence file:
   `./analyzer /home/user/primers.fasta`
   This will output the calculated integral of the alignment score probability density function. Since it is a normalized PDF, the analytical solution is 1.0. Your numerical integration should be very close to this.

4. **Identify the Bottleneck:**
   Use `go tool pprof` to analyze `/home/user/cpu.prof`. Identify the function *within the `main` package* that consumes the highest cumulative CPU time.

5. **Report:**
   Create a JSON file at `/home/user/report.json` with the following format:
   ```json
   {
     "integral_value": <float, rounded to 4 decimal places>,
     "bottleneck_function": "<name of the function in the main package consuming the most CPU time>"
   }
   ```
   Example: `"bottleneck_function": "main.CalculateGC"`

Ensure all files are correctly placed and the report JSON strictly follows the keys specified above.