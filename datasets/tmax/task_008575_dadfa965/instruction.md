You are a data scientist fitting structural models to protein data.

You have a simplified Protein Data Bank (PDB) file located at `/home/user/protein.pdb` and a reference dataset of structural models at `/home/user/reference_models.csv`.

Your task is to:
1. Parse `/home/user/protein.pdb` to extract the Z-coordinates of all C-alpha atoms. In this file, lines starting with the word `ATOM` and having `CA` as the exact 3rd space-separated field represent these atoms. The Z-coordinate is the 8th space-separated field.
2. Treat the extracted Z-coordinates as a sequential spatial signal $y_i$, where the independent variable $x_i$ is the 1-based index of the extracted CA atom in the sequence (i.e., $x = 1, 2, 3, \dots, N$).
3. Perform a simple linear regression to find the line of best fit $y = m x + c$, where $m$ is the slope and $c$ is the y-intercept.
4. Read the reference dataset `/home/user/reference_models.csv`, which contains a header row and follows the format `ModelName,Slope,Intercept`.
5. For each model in the reference dataset, calculate the Euclidean distance to your fitted parameters in the $(m, c)$ parameter space: $Distance = \sqrt{(m - Slope)^2 + (c - Intercept)^2}$.
6. Identify the model with the minimum distance to your fitted parameters.
7. Write ONLY the exact name of the best-matching model to a new file `/home/user/best_model.txt`.

You must perform this task using Bash commands and standard Linux utilities (like `awk`, `sed`, `grep`) or a short script written directly in the terminal.