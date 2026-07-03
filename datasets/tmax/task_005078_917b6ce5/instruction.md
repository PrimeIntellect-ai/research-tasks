You are a performance engineer profiling a scientific simulation that has been producing non-reproducible probability distributions due to floating-point reduction order issues.

We have an audio file located at `/app/data/target_metric.wav`. It contains a short spoken phrase specifying the expected reference distance metric for our analytical validation (e.g., "zero point zero five").

Your task is to write and run a Python HTTP server that acts as a simulation validation service. 

Requirements:
1. The server must listen on `127.0.0.1:8000`.
2. It must expose a single HTTP GET endpoint at `/api/validate`.
3. When the endpoint is hit, the server must:
   - Generate a 2D numpy array of `float32` of size 1000x1000, filled with uniform random numbers in [0.0, 1.0) using `numpy.random.default_rng(seed=42)`.
   - To fix the reduction order precision issues, cast the array to `float64` before summing along axis 1. 
   - Normalize the resulting 1D array of size 1000 so that it sums to 1.0, treating it as a probability distribution $P$.
   - Construct a reference probability distribution $Q$ of size 1000, where every element is $1/1000$.
   - Compute the Kullback-Leibler (KL) divergence from $Q$ to $P$, i.e., $D_{KL}(P \parallel Q) = \sum P(i) \log(P(i) / Q(i))$.
   - Read/transcribe the numerical value spoken in `/app/data/target_metric.wav` (you may install and use any Python speech recognition libraries like `SpeechRecognition` to transcribe this, or use standard CLI tools if you prefer).
   - Return a JSON response exactly in this format:
     ```json
     {
       "computed_kl_divergence": <float_value>,
       "expected_metric": <float_value_from_audio>
     }
     ```

Leave the server running in the background or foreground so that we can query `http://127.0.0.1:8000/api/validate` to verify your solution.