You are a performance engineer tasked with debugging a pipeline that processes protein structures. 

We have a Go program, `/home/user/matrix_solver.go`, that performs spatial domain decomposition on a PDB (Protein Data Bank) file and generates a contact matrix for further factorization. However, the program currently crashes with a "near-singular matrix: division by zero" panic. 

Our profiling indicates this happens because the input file `/home/user/protein.pdb` contains duplicate ATOM records with the exact same X, Y, and Z coordinates, causing a distance of zero between distinct entries.

Your task:
1. Using standard bash/Unix tools (e.g., `awk`, `grep`, `uniq`), process `/home/user/protein.pdb` to remove duplicate ATOM lines based *strictly* on their 3D coordinates (columns 31 to 54 in the standard PDB format). Keep the first occurrence of any coordinate and preserve all non-ATOM header/footer lines exactly as they are.
2. Save the cleaned file to `/home/user/clean.pdb`.
3. Compile and run the Go program on the cleaned file: `go run /home/user/matrix_solver.go /home/user/clean.pdb > /home/user/solution.txt`.

Ensure `/home/user/solution.txt` is successfully generated and contains the final factorization output.