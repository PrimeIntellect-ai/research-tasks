You are a performance engineer testing a new structural biology analysis pipeline. 

There is a PDB file located at `/home/user/structure.pdb`.

Write a script in any suitable language (e.g., Python) to perform the following pipeline:
1. Parse the file to extract the X, Y, and Z coordinates of all `CA` (Alpha Carbon) atoms.
2. Construct an unweighted adjacency matrix representing a contact graph. An edge exists (value 1) if the Euclidean distance between two CA atoms is $\le 7.0$ Angstroms. All other entries should be 0. (The diagonal should be 1, as the distance from an atom to itself is 0).
3. Perform a matrix decomposition to compute the largest Singular Value of this adjacency matrix.
4. Output only the largest singular value, rounded to 2 decimal places.

Save your script as `/home/user/analyze.py`.

Once the script is written:
1. Execute the script and save the rounded largest singular value into `/home/user/top_sv.txt`.
2. Profile the script's resource usage using `/usr/bin/time -v python3 /home/user/analyze.py`. Redirect both standard output and standard error to `/home/user/profile.txt`.

Ensure all requested files are placed exactly as specified.