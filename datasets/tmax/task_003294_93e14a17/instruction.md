You are a bioinformatics analyst studying how sequence length affects the diffusion of a synthesized protein in a 1D capillary tube. We have recorded a reference experiment in a video file located at `/app/cell_video.mp4`.

Your task is to write a Go program that simulates a 1D numerical diffusion (Heat equation) based on a given biological sequence, using parameters extracted from the video file.

Here are the requirements for the simulator:
1. **Analyze the Video**: Inspect the video `/app/cell_video.mp4`. 
   - Let $W$ be the video's width in pixels. This will be the size of your 1D spatial mesh.
   - Let $F$ be the total number of frames in the video. This will be the number of time steps for your numerical solver.

2. **Bioinformatics Parsing**: Read standard input (`stdin`) until EOF. The input will be in FASTA format (potentially containing multiple sequence lines and a single header starting with `>`). Parse the input to extract the continuous biological sequence (ignoring the header and newlines). Let $L$ be the length (number of characters) of the extracted sequence.

3. **Numerical ODE/PDE Solving**:
   - Initialize a 1D float64 slice of size $W$ with all zeros.
   - Set the initial concentration at the center of the mesh (index `W / 2`, using integer division) to the sequence length $L$.
   - Simulate $F$ time steps of diffusion using the explicit finite difference method:
     `C_new[x] = C[x] + alpha * (C[x-1] - 2*C[x] + C[x+1])`
   - Use a diffusion coefficient $\alpha = 0.25$.
   - Enforce Dirichlet boundary conditions: the first and last elements of the mesh (index `0` and `W-1`) must always remain `0.0`.
   - Update the entire mesh synchronously for each of the $F$ time steps.

4. **Output**: After the $F$ steps are complete, print ONLY the final concentration at the center of the mesh (index `W / 2`), formatted to exactly six decimal places followed by a newline (e.g., using `fmt.Printf("%.6f\n", val)`).

Write your Go code in `/home/user/simulator.go` and compile it into an executable named `/home/user/solver`. Ensure it takes input from `stdin` and writes the result to `stdout`.