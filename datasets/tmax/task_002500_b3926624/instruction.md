You are a bioinformatics analyst working on modeling mRNA expression levels over time based on recent lab experiments. The principal investigator dictated the target mRNA concentrations into an audio recorder, but left the lab before running the analysis. 

Your task is to build a bash-based simulation and optimization pipeline to find the best kinetic parameters for the expression model, and serve the result via a simple web API.

**Step 1: Extract Experimental Data**
An audio recording of the dictated mRNA target concentrations at hours T=1, 2, 3, 4, and 5 is located at `/app/data/experiment_audio.wav`. 
You must transcribe this audio file to retrieve the five integer target values. You may use `whisper` (which is pre-installed in the environment) to transcribe the file.

**Step 2: Implement the ODE Model in Bash**
We model the mRNA concentration $M(t)$ using the following ordinary differential equation (ODE):
$dM/dt = k_1 - k_2 \cdot M$
where $k_1$ is the transcription rate and $k_2$ is the degradation rate. The initial condition is $M(0) = 0$.

Write a bash script `/home/user/model.sh` that takes two arguments: `k1` and `k2`. 
The script must simulate the ODE using Euler's method with a time step of $dt = 0.1$ from $t=0$ to $t=5.0$. 
The script should output the simulated concentration $M$ at $T=1.0, 2.0, 3.0, 4.0, 5.0$, one value per line, rounded to the nearest integer. Ensure you use standard CLI tools like `awk` or `bc` for the math.

**Step 3: Regression Testing**
Write a regression test script `/home/user/test_model.sh` that verifies `/home/user/model.sh 10 0.5`. If the output does not perfectly match the analytically expected integer values for those parameters at T=1,2,3,4,5, it should exit with a non-zero status.

**Step 4: Parallel Grid Search Optimization**
Use GNU `parallel` to run a grid search over the parameter space to find the $(k_1, k_2)$ pair that minimizes the Sum of Squared Errors (SSE) between your simulated $M(t)$ and the five target values transcribed from the audio.
The search grid must be:
- $k_1 \in \{10, 15, 20, 25, 30, 35, 40, 45, 50\}$
- $k_2 \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0\}$

**Step 5: Multi-Protocol Serving**
Once the optimal $k_1$ and $k_2$ are found, expose them via a lightweight HTTP server written purely in Bash (using `nc` or `socat`). 
The server must:
- Bind to `0.0.0.0:8080`
- Listen continuously for incoming connections
- When it receives an HTTP `GET /result` request, it must respond with a valid `200 OK` HTTP header and a JSON payload containing the optimal parameters, exactly in this format: `{"k1": X, "k2": Y.Y}`.

Keep the server running in the background. Note: the evaluation script will test the `GET /result` endpoint on port 8080.