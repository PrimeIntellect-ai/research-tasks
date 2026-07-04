You are an analyst in a bioinformatics lab. The principal investigator left an audio recording of laboratory notes detailing the specific numerical parameters required to calibrate our primer filtering pipeline. Due to a recent equipment failure, the original written notes were lost, and all we have is the audio file located at `/app/lab_notes.wav`.

Your task is to build a robust, parallelized sequence filtering tool in Python that processes potential primer sequences and filters out those that would cause our downstream polymerase extension simulation (a numerical integrator) to diverge.

Step 1: Extract the parameters
Transcribe the audio file at `/app/lab_notes.wav`. The audio contains two critical floating-point parameters, `Alpha` and `Beta`.

Step 2: Solve the stability equation
The numerical integrator's stability boundary is defined by the root of the following nonlinear equation:
$x^3 - \text{Alpha} \cdot x^2 + \text{Beta} \cdot \ln(x) - 10 = 0$
Find the root $x$ (for $x > 1$). The maximum allowable GC-content percentage for a stable primer is exactly $C = \text{floor}(x \times 10)$.

Step 3: Create the Filter
Write a Python script at `/home/user/filter_primers.py`.
The script must take an input directory containing FASTA files and an output directory:
`python3 /home/user/filter_primers.py <input_dir> <output_dir>`

The script must:
1. Use Python's multiprocessing (or mpi4py) to process multiple FASTA files in parallel.
2. Read each `.fasta` file from the `<input_dir>`.
3. Calculate the GC-content percentage of each sequence ( (G + C) / total_length * 100 ).
4. If the GC-content is less than or equal to $C$, keep the sequence.
5. Write the valid sequences to files of the same name in the `<output_dir>`.

To verify your script, run it against the mixed datasets provided by the lab. Your script must process the files efficiently and accurately separate the viable primers from those that cause divergence.