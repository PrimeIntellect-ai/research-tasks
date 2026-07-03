You are an algorithmic data scientist tasked with building a robust hypothesis testing and sampling pipeline in Bash. 

We have a legacy toolset located at `/app/stats-tools/` which includes a fast C-based MCMC sampler for estimating posteriors when standard parametric models fail (e.g., when distributions heavily diverge, analogous to a matrix factorization failing on near-singular input).

**Phase 1: Fix the Vendored Package**
The `/app/stats-tools/` package contains a `Makefile` and source code, but it currently fails to build. 
1. Diagnose and fix the build issue in `/app/stats-tools/Makefile` (you may use standard tools like `gcc` and `make`). 
2. Successfully compile the `mcmc_estimate` binary.

**Phase 2: Build the Orchestrator**
Write a pure Bash script (using standard CLI tools like `awk` and `bc`) at `/home/user/analyze.sh` that orchestrates a hypothesis comparison workflow.
The script must accept exactly 4 integer arguments: `O1` `O2` `E1` `E2`. (O = Observed frequencies, E = Expected frequencies).

Implement the following logic:
1. If either `E1` or `E2` is equal to `0`, the script must print exactly: `ERROR: Zero expectation` and exit cleanly.
2. Calculate the Chi-square distance metric between the observed and expected distributions:
   `Chi2 = (O1 - E1)^2 / E1 + (O2 - E2)^2 / E2`
3. If the computed `Chi2` is strictly less than `4.00`:
   Print `ACCEPT: ` followed by the Chi2 value formatted to exactly two decimal places (e.g., `ACCEPT: 1.25`).
4. If the computed `Chi2` is greater than or equal to `4.00`, the basic null hypothesis fails. You must fallback to MCMC estimation to sample the posterior:
   Invoke the fixed tool: `/app/stats-tools/mcmc_estimate O1 O2 E1 E2`
   Capture its output, and print: `REJECT: ` followed by the tool's output.

Ensure your script is marked executable. Your script will be aggressively fuzzed against a secret oracle to ensure bit-exact equivalence on all branching paths, floating-point calculations, and formatting.