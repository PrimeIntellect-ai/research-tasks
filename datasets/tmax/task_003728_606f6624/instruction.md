You are a performance engineer working in a structural bioinformatics lab. Your team is analyzing the 3D conformations of nucleotide sequences, and a researcher has developed a custom "Sequence-Structure Pairwise Distance" metric. 

The metric takes a sequence and a list of 3D coordinates, computes the pairwise Euclidean distance matrix for all coordinates, and applies custom weighting based on sequence character matches/mismatches, finally returning the sum of the weighted matrix.

Currently, the researcher's reference script `/app/slow_metric.py` works but is extremely slow for large multidimensional arrays due to deeply nested Python loops. Your task is to write an optimized version of this script.

Here are the requirements:

1. **Audio Transcription**: The exact scaling weights (`alpha` for matches, `beta` for mismatches) for the distance metric were left in a voice memo by the researcher at `/app/dictation.wav`. You must transcribe this audio file to find the correct `alpha` and `beta` values.
2. **Notebook Profiling**: First, orchestrate a brief profiling workflow. Create a Jupyter notebook at `/home/user/profile_workflow.ipynb` that uses Python's `cProfile` to analyze `/app/slow_metric.py` on a dummy JSON input (with at least 50 coordinates/bases). 
3. **Optimized Implementation**: Write a highly optimized program at `/home/user/fast_metric.py`.
   - **Input**: Reads a JSON string from standard input (`stdin`). The JSON has the format: `{"sequence": "ACGT...", "coords": [[x1, y1, z1], [x2, y2, z2], ...]}`. The length of the sequence will exactly match the number of coordinates.
   - **Output**: Prints only a single floating-point number to standard output (`stdout`), representing the total sum of the weighted distance matrix, rounded to 4 decimal places.
   - **Logic**: For every pair of indices `(i, j)`, calculate the Euclidean distance between `coords[i]` and `coords[j]`. If `sequence[i] == sequence[j]`, multiply the distance by `alpha`. If they do not match, multiply by `beta`. Sum all these weighted distances.
   - **Performance**: You are encouraged to use vectorized operations (e.g., NumPy or similar) to achieve high performance.

Our automated testing suite will rigorously fuzz your `/home/user/fast_metric.py` against a hidden compiled oracle by sending hundreds of random sequences and multi-dimensional coordinate arrays to `stdin` and verifying bit-exact output equivalence.