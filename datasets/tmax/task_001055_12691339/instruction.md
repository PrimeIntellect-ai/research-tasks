You are an MLOps engineer tasked with tracking experiment artifacts and reproducing a legacy data processing pipeline. 

We have a legacy, stripped binary located at `/app/legacy_embedder` that takes a text file as input and outputs a raw binary file containing 64-dimensional float32 vector embeddings. We need to replace this black-box binary with a reproducible Python pipeline.

Here is your multi-stage objective:

1. **Environment Setup & Binary Analysis**:
   - Analyze `/app/legacy_embedder`. It reads a plain text file (one sentence per line) and writes a `.bin` file containing `N` 64-dimensional float32 vectors (where `N` is the number of lines).
   - A dataset of 100 test sentences is located at `/home/user/data/eval.txt`. Generate the ground truth embeddings using the legacy binary.

2. **Embedding Pipeline Reproducibility**:
   - Write a Python script `/home/user/reproduce_embeds.py` that reads `/home/user/data/eval.txt` and implements the following embedding logic: 
     - Create a basic bag-of-words character trigram count vector for each sentence.
     - Project it into 64 dimensions using a deterministic random projection matrix. (Seed the `numpy` random generator with `42` before generating the 64 x `vocab_size` projection matrix).
     - Save the output as `/home/user/data/python_embeds.bin` in the exact same binary float32 format as the legacy binary.
   - *Note: The legacy binary uses this exact algorithm with seed 42, but we lost the source code.*

3. **Model Output Validation & Plotting**:
   - We have an existing plotting script `/home/user/plot_artifacts.py` which computes the Mean Squared Error (MSE) between the legacy embeddings and your Python embeddings, and generates a scatter plot of the residuals saved to `/home/user/residual_plot.png`.
   - **Issue:** Currently, running `/home/user/plot_artifacts.py` crashes or produces a completely blank plot due to a matplotlib backend misconfiguration in our headless server environment.
   - Fix the script so it correctly renders and saves the plot without requiring an interactive display.

4. **Deliverables**:
   - `/home/user/data/python_embeds.bin` (Must closely match the legacy binary's output).
   - A fully functional, fixed `/home/user/plot_artifacts.py` that outputs a visually correct `/home/user/residual_plot.png`.

Your success will be evaluated by an automated verifier that computes the structural similarity (SSIM) of your generated plot against a reference plot, as well as the Mean Squared Error between your `.bin` output and the reference embeddings.