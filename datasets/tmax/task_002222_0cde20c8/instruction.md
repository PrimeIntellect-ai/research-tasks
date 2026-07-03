You are an environmental data scientist fitting a detection model to identify engineered genetic anomalies in water samples. You have been provided with an expected baseline model and a set of test samples. However, malicious actors are actively trying to spoof the sensor by submitting synthetic sequences ("evil" corpus) that mimic the length and basic composition of natural samples ("clean" corpus).

Your objective is to create a robust C-based filtering tool that successfully rejects all synthetic sequences while accepting all natural ones.

Here are your steps:

1. **Video Threshold Extraction:** 
   There is a calibration video located at `/app/calibration_timelapse.mp4`. This video records a liquid handling assay's fluorescence. The video shows a circular well that starts dark and gradually becomes brighter before reaching a stable plateau intensity. 
   - Extract the frames of this video using `ffmpeg`.
   - Calculate the steady-state average pixel intensity (grayscale value from 0 to 255) of the final 10 frames.
   - Divide this average grayscale value by 255.0 to get a normalized value `T`. `T` is your critical decision threshold.

2. **Reference Model Loading:**
   The file `/app/reference_model.h5` is an HDF5 file containing the expected "healthy" dinucleotide transition probability matrix (a 4x4 array of `double` representing the probabilities of A, C, G, T followed by A, C, G, T). It is stored under the dataset name `/dinucleotide_probs`.

3. **Classifier Implementation:**
   Write a C program (e.g., `detector.c`) that evaluates a given FASTA file. Your program must take two arguments: the path to the HDF5 reference file and the path to a FASTA file.
   - It must parse the given `.fasta` file and calculate the empirical 4x4 dinucleotide transition probability matrix.
   - It must compute the **Bhattacharyya distance** between the FASTA's empirical distribution and the reference distribution loaded from the HDF5 file.
   - Because single-point estimates are noisy, your program must generate a **95% Bootstrap Confidence Interval** for this distance. To do this, perform 1000 bootstrap iterations: in each iteration, resample the sequences in the FASTA file with replacement (keeping the number of sequences equal to the original file), recalculate the empirical matrix, and compute the Bhattacharyya distance.
   - Find the lower bound of the 95% confidence interval (the 2.5th percentile of the bootstrap distances). 
   - If this lower bound is **greater than** your threshold `T` (extracted from the video), the sample is highly anomalous. The program should output `REJECT` and exit with code 1.
   - Otherwise, the program should output `ACCEPT` and exit with code 0.

4. **Corpus Validation:**
   We have provided two directories of FASTA files:
   - `/app/corpus/clean/` : Contains natural samples. Your program MUST accept (exit code 0) 100% of these.
   - `/app/corpus/evil/` : Contains synthetic samples. Your program MUST reject (exit code 1) 100% of these.

Write a bash script `/home/user/run_eval.sh` that compiles your C program (ensure you link HDF5 and math libraries, e.g., `-lhdf5 -lm`) and iterates over all files in `/app/corpus/clean/` and `/app/corpus/evil/`, running your detector on each. Log the results to `/home/user/eval_results.txt` with lines formatted exactly as:
`[ACCEPT|REJECT] /path/to/file.fasta`

Ensure your C code is efficient and strictly adheres to standard C.