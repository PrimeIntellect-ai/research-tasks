I am a researcher running protein structure simulations, and I need your help executing a workflow in my Linux environment. I have a Jupyter notebook that orchestrates my pipeline, but I don't have Jupyter or Python installed on this server. I need you to orchestrate this using only Bash and standard CLI tools (like `jq`, `awk`, `sed`, etc.).

Here is what you need to do:

1. **Extract the Workflow**: 
   There is a Jupyter notebook located at `/home/user/workflow.ipynb`. It contains exactly one code cell with Bash commands. Use `jq` to extract the source lines of this code cell and save it as an executable bash script at `/home/user/run_pipeline.sh`.

2. **Write the Signal Processing Script**:
   The extracted pipeline expects an executable script named `/home/user/analyze_spectra.sh` to exist. You must write this script in pure Bash/Awk. 
   
   The script `/home/user/analyze_spectra.sh` must take exactly one argument: the path to a FASTA file. It should:
   - Read the FASTA file, ignoring the header line (starts with `>`), and concatenate the remaining lines to get the full amino acid sequence.
   - Convert the sequence into a discrete numeric signal $x[n]$ (0-indexed) representing hydrophobicity, using this mapping:
     - Hydrophobic (`A`, `I`, `L`, `M`, `F`, `W`, `V`) $\rightarrow 1.0$
     - Polar/Charged (`R`, `N`, `D`, `E`, `Q`, `K`, `S`, `T`) $\rightarrow -1.0$
     - Any other character $\rightarrow 0.0$
   - Compute the Discrete Fourier Transform spectral power for the alpha-helix frequency $f = 0.2777$. 
     The power $P$ is calculated as:
     $X = \sum_{n=0}^{L-1} x[n] \cos(2\pi f n)$
     $Y = \sum_{n=0}^{L-1} x[n] \sin(2\pi f n)$
     $P = X^2 + Y^2$
     *(Use $\pi = 3.14159265359$)*
   - Print the final power $P$ rounded to exactly 2 decimal places to standard output.

3. **Execute the Pipeline**:
   Once you have created `/home/user/analyze_spectra.sh`, run the `/home/user/run_pipeline.sh` script you extracted. It will process the FASTA file at `/home/user/protein.fasta` and write the result to `/home/user/spectral_output.txt`.

Ensure all scripts are executable and the final power value is correctly formatted in the text file.