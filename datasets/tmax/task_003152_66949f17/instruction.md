You are tasked with setting up a bioinformatics simulation service. We have an audio dictation from a researcher specifying a protein sequence, and we need a high-performance Monte Carlo simulation service written in Rust to compute its expected polymer properties.

Here are your instructions:

1. **Audio Transcription**: 
   An audio file is located at `/app/dictation.wav`. It contains a researcher dictating a sequence of amino acids. Transcribe the audio and convert the amino acid names to their standard 1-letter codes. Save this sequence as a valid FASTA file at `/home/user/target.fasta`.

2. **Rust Simulation Server**:
   Create a new Rust project and write an HTTP server that listens on `127.0.0.1:8080`. 
   The server must expose a POST endpoint at `/simulate`.
   
   The `/simulate` endpoint will receive a JSON payload of the form:
   `{"fasta_path": "/path/to/file.fasta", "iterations": 100000}`

3. **Monte Carlo Simulation Details**:
   When the endpoint is called, the server must:
   - Parse the sequence from the provided FASTA file.
   - Perform a Monte Carlo simulation of a 3D ideal freely-jointed chain (random walk).
   - The chain starts at `(0.0, 0.0, 0.0)`.
   - For each amino acid in the sequence, the chain takes one step in a uniformly random 3D direction.
   - The step length depends on the amino acid: 
     * Alanine (A) = 1.0
     * Cysteine (C) = 2.0
     * Aspartic Acid (D) = 3.0
     * Phenylalanine (F) = 4.0
     * Glycine (G) = 5.0
     * (Any other amino acid has a step length of 0.0)
   - Run the simulation for the specified number of `iterations`. Each iteration is an independent random walk of the entire sequence.
   - For each walk, compute the squared end-to-end distance ($R^2 = x^2 + y^2 + z^2$).
   - Calculate the mean of these squared distances across all iterations.
   
4. **Response Format**:
   The endpoint must return a JSON response containing the average squared end-to-end distance:
   `{"mean_sq_dist": 54.98}` (example value).

5. **Execution**:
   Compile your Rust server in release mode (`cargo build --release`) and start it. Ensure the server process remains running in the background so it can be queried by our automated regression testing tools.