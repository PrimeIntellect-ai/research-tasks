You are an AI assistant helping a computational chemistry researcher. 

I have a set of simulated molecular networks and their corresponding Raman spectroscopy signals. I need you to build a reproducible bash-only pipeline (using standard coreutils like `awk`, `grep`, `sort`, `tr`, etc.) to filter these molecules and extract specific signal features.

The data is located in `/home/user/data/`:
1. `/home/user/data/graphs/`: Contains undirected graph edge lists representing the molecular networks (`<molecule_name>.edgelist`). Each line has two space-separated integers representing an edge between two atoms.
2. `/home/user/data/spectra/`: Contains the corresponding Raman spectra (`<molecule_name>.dat`). Each file has two space-separated columns: `Frequency` (cm⁻¹) and `Intensity` (arbitrary units).

Please create and run a reproducible shell script at `/home/user/pipeline.sh` that performs the following steps:
1. Iterate through all `.edgelist` files in alphabetical order.
2. Calculate the degree of each node in the undirected graph. (Note: an edge `1 2` means both node 1 and node 2 have an edge).
3. Identify molecules where the *maximum degree* of any node in the molecule is **exactly 4** (representing a quaternary carbon-like center).
4. For these identified molecules, analyze their corresponding `.dat` spectrum file.
5. Find the peak (maximum `Intensity`) that occurs strictly within the `Frequency` range `1000` to `2000` (inclusive).
6. Output the results to `/home/user/results.tsv` in a tab-separated format with exactly four columns:
   `molecule_name`    `max_degree`    `peak_frequency`    `peak_intensity`

Example of an expected row in `/home/user/results.tsv`:
`mol_X    4    1550    82.5`

Ensure your script processes the data and generates the `/home/user/results.tsv` file exactly as specified.