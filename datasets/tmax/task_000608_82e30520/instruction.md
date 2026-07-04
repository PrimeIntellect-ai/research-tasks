You are a performance engineer optimizing a bioinformatics data processing pipeline. The pipeline currently uses slow legacy binaries to analyze spectroscopy signals and run Monte Carlo simulations. Your goal is to extract experimental data, process structural files, and rewrite a critical simulation component into a highly optimized Bash script.

**Part 1: Spectroscopy Video Analysis**
An experiment was recorded and saved as `/app/spectroscopy_run.mp4`. 
1. Use `ffmpeg` to extract the frames from this video.
2. For each frame (in sequential order), calculate the average grayscale brightness (from 0 to 255) of the entire frame. 
3. Save the results to `/home/user/frame_brightness.csv` with the format `frame_index,average_brightness` (e.g., `0,12.5` - precise to one decimal place). 

**Part 2: Bioinformatics Parsing**
You must extract an initialization parameter from a molecular structure file located at `/app/target.pdb`.
1. Parse the PDB file and count the exact number of `HETATM` records.
2. Save this integer value to `/home/user/hetatm_count.txt`.
Let this count be known as $K$.

**Part 3: Monte Carlo Simulator Optimization**
A legacy binary at `/app/oracle_mc_sim` is used to simulate molecular collisions based on a DNA sequence. It is extremely slow. 
Your task is to write a highly optimized, bit-exact equivalent script at `/home/user/fast_mc_sim.sh`.

The algorithm used by the oracle is a deterministic Monte Carlo integration to estimate a collision metric. Here is the exact specification:
- The script takes two arguments: a DNA sequence (string) and the parameter $K$ (integer). Example: `/home/user/fast_mc_sim.sh "ACGT" 42`
- It simulates $N$ random 2D points, where $N$ is the length of the DNA sequence multiplied by $K$.
- It uses a Linear Congruential Generator (LCG) to generate coordinates. 
  - $X_n = (1103515245 \times X_{n-1} + 12345) \pmod{2^{31}}$
  - The initial seed $X_0$ is the sum of the ASCII values of all characters in the DNA sequence, plus $K$.
- For each of the $N$ points, generate two consecutive LCG values to represent the $(x, y)$ coordinates. (So $2N$ LCG iterations total).
- A collision occurs if $(x / 2^{31})^2 + (y / 2^{31})^2 \le 1$.
- The script must output a single integer to standard output: the total number of collisions.

Your script `/home/user/fast_mc_sim.sh` must be written in Bash (using utilities like `awk` is highly recommended for performance). An automated fuzz-equivalence verifier will test your script against `/app/oracle_mc_sim` with thousands of random DNA strings. Both implementations must produce identical outputs.

Ensure your script has executable permissions (`chmod +x /home/user/fast_mc_sim.sh`).