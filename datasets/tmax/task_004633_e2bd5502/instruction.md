You are a data scientist debugging a bash-based signal processing pipeline for a bioinformatics project. 

The system consists of two services running in the background:
1. A lightweight Python HTTP server on port 8000 that serves biological signal data.
2. A Redis server on port 6379 used to cache expected reference values.

Currently, our bash script `/home/user/compute_integral.sh` is supposed to download a signal file, parse it, and compute the area under the curve (numerical integration) using the Trapezoidal rule. However, the current implementation assumes a constant step-size between data points, which causes divergence and incorrect results because our sensors use adaptive sampling (variable step-sizes).

Your task:
1. Fix the script `/home/user/compute_integral.sh` so that it correctly computes the numerical integral for variable step sizes. 
2. The script must accept a single argument: the path to a local input file. (During production, it downloads the file, but for testing, it reads a local file passed as `$1`).
3. The input file format starts with a FASTA-like header `>Signal_ID`, followed by lines of `time value` pairs (both floating-point numbers). Ignore the header.
4. Output ONLY the final computed integral, rounded to exactly 4 decimal places (e.g., `12.3456`).
5. Ensure your script is robust and implemented entirely using standard bash tools (like `awk`, `sed`, `bc`).
6. To demonstrate it works in the service context, write a wrapper `/home/user/test_flow.sh` that queries `http://127.0.0.1:8000/signal/test1`, saves it to `/tmp/test1.dat`, runs your fixed `compute_integral.sh` on it, and sets the result in Redis with the key `integral:test1`.

Your integration script will be strictly verified for mathematical correctness against an oracle implementation using thousands of randomly generated variable-step signals.