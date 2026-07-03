You are a bioinformatics analyst tasked with determining the composition of an environmental DNA sample. The sample contains a mixture of k-mer profiles from two known reference species.

I have provided an HDF5 file located at `/home/user/data/profiles.h5`. This file contains three datasets:
1. `reference_A`: The k-mer frequency profile for Species A (1D array).
2. `reference_B`: The k-mer frequency profile for Species B (1D array).
3. `target_sample`: The k-mer frequency profile of the environmental sample (1D array).

The `target_sample` is a linear mixture of `reference_A` and `reference_B`, plus some random biological noise. The relationship can be modeled as:
`mixture = alpha * reference_A + (1 - alpha) * reference_B`

Your task:
1. Write a Python script to read the datasets from the HDF5 file. (You may need to install `h5py` and `scipy` if they are not already installed).
2. Use an optimization algorithm (e.g., using `scipy.optimize.minimize` or standard least-squares) to find the mixing parameter `alpha` (where 0 <= alpha <= 1) that minimizes the Mean Squared Error (MSE) between your calculated `mixture` and the `target_sample`.
3. Save the resulting optimized `alpha` value to a JSON file at `/home/user/result.json`. The JSON file must have exactly this format, with the value rounded to 4 decimal places:
```json
{"alpha": 0.1234}
```