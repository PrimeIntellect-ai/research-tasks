Hello, I am a researcher running spectroscopy simulations. I have a Python script located at `/app/spectral_denoise.py` that processes a large dataset of simulated spectral matrices (`/app/raw_spectra.npy`). The script performs noise reduction by applying Singular Value Decomposition (SVD) and truncating the singular values. 

Currently, the script runs sequentially and takes too long. I need you to do the following:

1. Extract the required SVD truncation parameter `k` from my handwritten memo image located at `/app/config_memo.png`. You will need to use an OCR tool (like `tesseract`) to read the parameter. It is written in the format `SVD_TRUNCATION_K=...`.
2. Modify `/app/spectral_denoise.py` to use `mpi4py` to parallelize the processing of the spectral data across 4 MPI ranks. The dataset contains 1000 matrices; distribute them evenly among the ranks.
3. Apply the SVD decomposition, truncate to the `k` largest singular values, reconstruct the matrices, and gather them back.
4. Save the final denoised dataset to `/home/user/output_spectra.npy`.
5. Measure the total execution time of the `mpi4py` processing and write just the elapsed time in seconds (as a float) to `/home/user/timing.log`.

To ensure your parallel implementation is correct, I have provided a reference dataset at `/app/reference_spectra.npy`. Your output must mathematically match this reference dataset (MSE < 1e-8). Additionally, your parallelized script must achieve a significant speedup compared to the serial version.

Run your script using `mpirun -n 4 python /app/spectral_denoise.py` to test it.