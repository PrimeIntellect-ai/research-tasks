You are an AI assistant helping a computational biologist fix a reproducibility issue in their simulation pipeline.

The researcher is running a Monte Carlo-based script to evaluate protein conformations. They have noticed that the final total score calculated from the simulation runs varies slightly between different machines and runs, despite individual run scores being identical. They suspect this is due to floating-point addition reduction order. Adding floating-point numbers of varying magnitudes in a non-deterministic order (like the arbitrary output of `find`) causes precision loss differences.

Your task:
1. Parse the provided PDB file `/home/user/data/protein.pdb`. Extract only the X, Y, and Z coordinates (columns 6, 7, and 8, assuming space-separated fields) for atoms where the record type is `ATOM` and the atom name is `CA`. Save these coordinates (space-separated) to `/home/user/ca_coords.txt`.
2. Run the existing simulation script `/home/user/mc_sim.sh`. This script will read `/home/user/ca_coords.txt` and generate 100 output files in `/home/user/results/`, each containing a single floating-point score.
3. Fix the reduction script `/home/user/reduce.sh`. Currently, it uses `find` to read all `.score` files and sum them using `awk`, which processes them in a non-deterministic order. Modify `/home/user/reduce.sh` so that it first extracts all the floating-point values from the files, **sorts them numerically from smallest to largest**, and *then* pipes them to `awk` to calculate the sum. The script should still output the final sum to `stdout` formatted to 15 decimal places (`%.15f\n`).
4. Run your fixed `/home/user/reduce.sh` and redirect its output to `/home/user/final_sum.txt`.
5. Create a simple text-based data visualization (histogram) of the individual scores. Count how many scores fall into the following intervals: `< 0.0`, `0.0 to 10.0` (inclusive of 0.0, exclusive of 10.0), `10.0 to 100.0` (inclusive of 10.0, exclusive of 100.0), and `>= 100.0`. Write the counts to `/home/user/histogram.txt` in exactly this format:
```
bin1_lt_0: [count]
bin2_0_10: [count]
bin3_10_100: [count]
bin4_ge_100: [count]
```

Please perform these steps using only Bash shell tools (`awk`, `grep`, `sort`, `find`, etc.).