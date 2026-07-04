You are a performance engineer working on a molecular dynamics simulation pipeline. Your team uses a Python script, `/home/user/md_analysis.py`, to calculate the total simplified Lennard-Jones potential energy for all Alpha-Carbon (CA) atoms in a given protein conformation.

The script reads a PDB file (`/home/user/protein_frame.pdb`) and computes the pairwise energy. However, the current implementation has two major issues:
1. **Non-reproducibility:** It uses `concurrent.futures.ThreadPoolExecutor` and aggregates results as they complete (`as_completed`). Because floating-point addition is not strictly associative, the order of chunk completion alters the final sum at the trailing decimal places. 
2. **Poor Performance:** The pairwise distances and energies are calculated using nested Python loops within the threads, which is highly inefficient.

Your task is to fix and optimize the script:
1. Rewrite the calculation in `/home/user/md_analysis.py` to be strictly reproducible and highly performant. 
2. Remove the threading and Python loops entirely. Instead, use NumPy multi-dimensional array manipulation and vectorization to compute the pairwise distances and the total energy. (Compute the energy only for unique pairs $i < j$).
3. The simplified Lennard-Jones formula to use for every pair of CA atoms $i$ and $j$ is:
   $E = \sum_{i < j} \left( \frac{1}{r_{ij}^{12}} - \frac{1}{r_{ij}^6} \right)$
   where $r_{ij}$ is the Euclidean distance between atom $i$ and atom $j$.
4. Ensure you only parse lines starting exactly with `ATOM` and where the atom name (characters 13-16 in standard PDB format, stripped of whitespace) is exactly `CA`.
5. Execute your optimized script. Write the final calculated total energy to `/home/user/energy_result.txt`, formatted to exactly 8 decimal places (e.g., `-123.45678901`).
6. Profile your final optimized script using the built-in `cProfile` module and save the profiling output to `/home/user/profile.prof`.

Ensure all file paths are strictly adhered to. You have root access to install any missing dependencies via `apt` or `pip` if necessary, though standard data science libraries are recommended.