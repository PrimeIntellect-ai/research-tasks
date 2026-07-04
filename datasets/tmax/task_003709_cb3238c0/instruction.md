You are acting as a research assistant for a computational biology lab. The lab has been using a generative AI model to predict protein conformations. However, the model sometimes hallucinates non-physical geometries that cannot exist in 3D space. You need to write a Python CLI tool to filter these out.

The model outputs custom `.pdist` files. Each file contains:
1. A FASTA-like header line starting with `>` followed by the sequence ID and the amino acid sequence (e.g., `>Seq1 MKVLY...`).
2. Subsequent lines describing the pairwise Euclidean distances between the Alpha-Carbon atoms of the sequence, in the format: `i j distance` where `i` and `j` are 0-indexed sequence positions. 

Your task is to write a Python script at `/home/user/filter_edm.py` that parses a given `.pdist` file, validates whether the pairwise distances form a mathematically valid Euclidean Distance Matrix (EDM) in 3D space, and exits with code `0` if it is valid (clean) or code `1` if it is physically impossible (hallucinated/evil).

To analytically validate an EDM:
1. Parse the `.pdist` file to construct the symmetric $N \times N$ distance matrix $D$. Ensure all missing diagonal elements are $0$ and the matrix is symmetrically populated.
2. Compute the squared distance matrix $D^{(2)}$ where each element is $D_{i,j}^2$.
3. Compute the centering matrix $J = I - \frac{1}{N} \mathbf{1} \mathbf{1}^T$, where $I$ is the identity matrix and $\mathbf{1}$ is a column vector of ones.
4. Compute the Gram matrix $G = -\frac{1}{2} J D^{(2)} J$.
5. A distance matrix is physically embeddable if and only if $G$ is positive semi-definite. You must perform a matrix decomposition (e.g., Eigendecomposition or SVD) on $G$ to find its eigenvalues.
6. Check if the minimum eigenvalue $\lambda_{min} \ge -\text{tolerance}$. If $\lambda_{min}$ is less than the negative tolerance, the structure is invalid.

**The Missing Parameter:**
The Principal Investigator left a voice memo detailing the exact floating-point tolerance you must use for the negative eigenvalues to account for floating-point inaccuracies in the generative model. You can find this audio file at `/app/audio/lab_memo.wav`. You will need to transcribe or listen to this file to obtain the precise tolerance value.

**Requirements:**
- Write your solution to `/home/user/filter_edm.py`.
- It must take exactly one positional argument: the path to the `.pdist` file.
- It must exit with `0` for valid structures and `1` for invalid structures.
- You can install any required Python packages (e.g., `numpy`, `scipy`) or system packages (e.g., `ffmpeg` for audio processing) as needed.
- Test your script thoroughly before concluding.