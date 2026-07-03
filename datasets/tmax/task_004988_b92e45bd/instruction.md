You are assisting a researcher with a structural biology simulation workflow. The researcher has left a voice memo detailing the parameters for the next step of the pipeline, but is currently unavailable. 

Your tasks are to:
1. Transcribe the audio file located at `/app/lab_notes.wav`. You may use standard tools available in the environment or install packages (e.g., via `pip install openai-whisper` or similar) to transcribe it.
2. The voice memo contains specific instructions on which protein chain to extract from `/app/target_complex.pdb`, the atoms to filter, the Gaussian kernel bandwidth to use for a 3D density estimation, the grid boundaries, and the HDF5 dataset name.
3. Write a C program (e.g., `compute_density.c`) that:
   - Parses `/app/target_complex.pdb` to extract the coordinates of the specified atoms for the specified chain.
   - Computes a 3D Kernel Density Estimation (KDE) using a Gaussian kernel on a 50x50x50 grid spanning the coordinates mentioned in the audio.
   - Uses the `HDF5` C library to output the resulting 3D density array (as a 3D dataset of IEEE 64-bit floats) into a file named `/home/user/density_out.h5` under the exact dataset name specified in the audio.
   - Writes the corresponding FASTA sequence of the extracted chain to `/home/user/extracted_chain.fasta`.
4. Compile your C program. You will likely need to install the HDF5 development libraries (e.g., `sudo apt-get update && sudo apt-get install -y libhdf5-dev`).
5. Run your program to produce `/home/user/density_out.h5` and `/home/user/extracted_chain.fasta`.

The final `density_out.h5` will be rigorously tested against a ground-truth reference HDF5 file. The Mean Squared Error (MSE) of the grid values must be below 1e-6.