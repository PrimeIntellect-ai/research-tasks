You are an ML engineer preparing a robust acoustic feature extraction pipeline for a speech recognition model. Your task involves recovering the label for a sample audio file and building a high-performance feature extractor in Rust.

**Step 1: Transcription (Labeling)**
You are provided with a raw audio file at `/app/speech.wav`. 
Extract the spoken text from this audio file and save the transcript (lowercase, stripped of punctuation) to `/home/user/transcript.txt`. You may install and use any Python libraries or tools (like `openai-whisper`) to accomplish this.

**Step 2: Acoustic Feature Extractor (Rust)**
Create a new Rust project at `/home/user/extractor`. You must implement a CLI tool that takes a sequence of raw audio samples and computes spectral features and energy statistics. 

Your compiled binary must be available at `/home/user/extractor/target/release/extractor`.
It must read standard input (stdin) until EOF, where each line contains a single `f32` audio sample. The input size will always be a multiple of 128 (between 1024 and 4096 samples).

The program must perform the following operations in order:
1. **Spectral Analysis (FFT):** Compute the 1D Fast Fourier Transform (unwindowed) of the entire input sequence. Extract the magnitudes of the first 16 bins (indices 0 through 15 inclusive).
2. **Matrix Projection (SVD):** A pre-computed 5x16 projection matrix is stored as comma-separated values at `/app/projection_matrix.txt` (5 rows, 16 columns). Multiply this matrix by the 16-dimensional magnitude vector (treated as a column vector) to produce a 5-dimensional feature vector.
3. **Bootstrap Confidence Interval:** Divide the original input signal into non-overlapping frames of 128 samples. Compute the energy of each frame (sum of squared sample values). Let `F` be the number of frames. Compute a 95% Bootstrap Confidence Interval for the *mean* frame energy using 1000 resamples. 
   * To ensure deterministic matching against our tests, generate random frame indices using this exact Linear Congruential Generator (LCG):
     State starts at `X = 42`.
     For each random draw: `X = (X * 1103515245 + 12345) % 2147483648`.
     The drawn index is `X % F`.
   * For each of the 1000 bootstrap iterations, draw `F` indices, collect those frame energies, and compute their mean. 
   * Sort the 1000 means. The 95% CI lower and upper bounds are the values at the 25th and 975th sorted indices (0-indexed).

**Output Format:**
Your program must print exactly two lines to standard output:
* Line 1: The 5 projected features, comma-separated, formatted to 4 decimal places (e.g., `1.2345,6.7890,...`).
* Line 2: The lower and upper bootstrap bounds, comma-separated, formatted to 4 decimal places (e.g., `0.1234,0.5678`).

**Validation:**
We have provided a reference oracle at `/app/oracle_extractor`. Your Rust program's output must be bit-exact equivalent to this oracle for any valid sequence of input floats. You should heavily test your executable against the oracle using randomly generated inputs before finishing.