You are an AI assistant helping a computational biologist who is trying to run a simplified simulation on a protein structure. The researcher wants to estimate the volume occupied by the protein using a Monte Carlo approach over a decomposed spatial grid, but their previous script failed due to near-singular input (division by zero when atoms share exact coordinates). 

Your task is to write a robust Bash script at `/home/user/simulate_mc.sh` that processes a PDB file, discretizes the space, and performs a Monte Carlo simulation. 

Here are the exact specifications for your script:
1. **Input**: The script must accept a single argument: the path to a PDB file.
2. **Bioinformatics Parsing**: Read only lines starting with `ATOM  ` (exactly `ATOM` followed by two spaces). Extract the X, Y, and Z coordinates. In PDB format, X is characters 31-38, Y is 39-46, and Z is 47-54 (1-based, inclusive).
3. **Domain Decomposition**:
   - Determine the bounding box of the protein: find the minimum and maximum X, Y, and Z values among all atoms.
   - If the bounding box has a dimension of size 0 (e.g., `maxX == minX`), artificially expand it by subtracting 0.1 from the minimum and adding 0.1 to the maximum for that dimension. This prevents division-by-zero errors (the near-singular failure).
   - Divide the bounding box into a 5x5x5 grid (125 total cells). 
   - Assign each atom to a grid cell `(i, j, k)` where `i`, `j`, `k` are integers from `0` to `4`. The formula for `i` is `floor(5 * (X - minX) / (maxX - minX))`. If `X == maxX`, assign it to index `4`. Do the same for `j` (using Y) and `k` (using Z).
   - Create a list of "occupied" cells (cells containing at least one atom).
4. **Monte Carlo Simulation**:
   - We want to estimate the fraction of bounding box volume occupied by the protein.
   - Using `awk`, initialize the random number generator with seed 42 (`srand(42)`).
   - Generate 1000 random spatial points within the bounding box. For each point, its X coordinate is `minX + rand() * (maxX - minX)`, and similarly for Y and Z.
   - For each random point, determine its cell `(i, j, k)` using the same grid logic.
   - If the point falls into a cell that is "occupied" by at least one atom, count it as a "hit".
5. **Output**:
   - The script must write exactly two lines to `/home/user/results.txt` in the following format:
     ```
     Occupied Cells: <number_of_unique_occupied_cells>
     MC Hit Ratio: <hits / 1000>
     ```

Make sure your script handles decimal arithmetic correctly (using `awk` is highly recommended for all math).
Do not use Python or any other language; the script must be written in Bash (calling standard Linux utilities like `awk`, `sed`, `grep`, `sort`, etc. is expected). Ensure the script is executable.

You can create a dummy PDB file to test your script before considering the task complete.