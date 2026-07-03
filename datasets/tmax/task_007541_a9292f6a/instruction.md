You are acting as a bioinformatics analyst. We have a Bash-based sequence scoring pipeline that attempts to find the optimal gap penalty for various DNA sequences using a custom gradient descent optimization implemented in pure Bash (relying on `bc` for floating-point math). 

Currently, our optimization script (`/home/user/optimizer.sh`) is failing. It diverges rapidly and produces wildly incorrect values or numeric overflow errors. This is due to a faulty step-size (learning rate) adaptation logic in the gradient descent loop.

Your task has three parts:

1. **Fix the Numerical Divergence:** 
   Inspect and modify `/home/user/optimizer.sh`. The script defines a scoring function where the optimal penalty `P` depends on the sequence length. Fix the gradient descent loop so that the step size decreases appropriately or stays sufficiently small, allowing it to converge accurately to the optimal penalty (where the gradient of the score is zero) instead of diverging.

2. **Run the Optimization:**
   We have a set of sequences in `/home/user/sequences.fasta`. For each sequence in the file, calculate its sequence length `L` (excluding the header line `>seqX`), and run your fixed `optimizer.sh <L>`. 

3. **Store in a Scientific Data Format (HDF5):**
   We need the final optimal penalty values stored efficiently for downstream analysis. Set up a local Python virtual environment in `/home/user/venv`, install `h5py`, and write a script to save the optimal penalties (in the order the sequences appear in the FASTA file) into an HDF5 file located at `/home/user/results.h5`. 
   
   The HDF5 file must contain a single 1D dataset named `/optimal_P` containing the optimal penalty values as 32-bit or 64-bit floats.

Ensure your entire pipeline runs successfully. Do not change the underlying biological scoring formula in `optimizer.sh`, only fix the optimization/step-size logic.