You are an MLOps engineer tasked with building a lightweight C-based feature extraction and inference pipeline to track machine states from audio sensors, and logging the experiment artifacts. 

We have recorded a test audio file located at `/app/machine_sound.wav` (16kHz, 16-bit mono PCM). The audio contains sounds of a machine alternating between "Idle" and "Active" states.

Your goal is to build an ETL and inference pipeline that processes this audio, computes a sequence of probabilities representing the machine's state using a recursive Bayesian filter, and benchmarks the inference performance.

**Step 1: ETL & Feature Extraction**
Write a C program (or use a combination of bash and C) to read the audio data. Process the audio in frames of exactly 1600 samples (100 milliseconds). 
For each frame, compute the Root Mean Square (RMS) amplitude:
`RMS = sqrt( (sum_{i=1}^{1600} x_i^2) / 1600 )`
where $x_i$ is the 16-bit signed integer sample value.

**Step 2: Probabilistic Modeling (Recursive Bayesian Filter)**
In your C program, implement a recursive Bayesian filter to estimate the probability that the machine is "Active" at each frame $t$.
*   **States:** Active ($A$), Idle ($I$).
*   **Initial Prior at $t=0$:** $P(A_0) = 0.1$, $P(I_0) = 0.9$.
*   **State Transition Probabilities:**
    *   $P(A_t | A_{t-1}) = 0.95$,  $P(I_t | A_{t-1}) = 0.05$
    *   $P(I_t | I_{t-1}) = 0.95$,  $P(A_t | I_{t-1}) = 0.05$
*   **Observation Model (Gaussian):**
    *   If Active: $E_t \sim \mathcal{N}(\mu = 5000, \sigma = 1000)$
    *   If Idle: $E_t \sim \mathcal{N}(\mu = 500, \sigma = 200)$
    *(Here $E_t$ is the RMS value of frame $t$)*

For each frame $t=1, 2, \dots$:
1. **Predict:** Compute the prior probability for frame $t$ based on the posterior of frame $t-1$ and the transition probabilities.
2. **Update:** Multiply the predicted probability by the likelihood of the observed RMS under each state's Gaussian PDF, then normalize so that $P(A_t) + P(I_t) = 1.0$.

**Step 3: Inference Benchmarking**
Wrap ONLY the Bayesian prediction and update logic (Step 2) in a timing block (e.g., using `clock_gettime` with `CLOCK_MONOTONIC`) to measure the total CPU time spent purely on inference across all frames. Exclude I/O and RMS calculation time.
Print the benchmarking result to standard output in the exact format:
`Average inference time per frame: [X.XXX] microseconds`

**Step 4: Experiment Artifact Output**
Create a directory `/home/user/artifacts`.
Save the computed posterior probabilities to `/home/user/artifacts/experiment_results.csv`.
The CSV must have a header `frame_index,prob_active` and one row per frame (0-indexed). Example format:
```csv
frame_index,prob_active
0,0.100000
1,0.082341
...
```

**Constraints:**
- Use C for the primary mathematical modeling and inference loop.
- Compile your code with standard optimizations (e.g., `-O3`).
- Do not use external machine learning or math libraries other than `<math.h>` and standard C libraries.