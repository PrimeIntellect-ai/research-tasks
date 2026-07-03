You are a data scientist building an automated anomaly detection service for mechanical audio data. You have been provided with an audio recording of a machine's operation at `/app/system_noise.wav`. 

Your goal is to build a mathematical feature extraction pipeline and expose it as a secure REST API.

Step 1: Feature Extraction & Matrix Decomposition
Write a Python script that reads `/app/system_noise.wav` (which is a mono, 16kHz WAV file).
1. Compute the Short-Time Fourier Transform (STFT) magnitude using `scipy.signal.stft` with `nperseg=256` and `noverlap=128`. Let this matrix be $S$ (frequencies $\times$ time frames).
2. Perform Singular Value Decomposition (SVD) on the magnitude matrix $S$. 
3. Reconstruct a rank-5 approximation of the spectrogram, $S_{approx}$, using only the first 5 singular values and their corresponding vectors.
4. Split $S_{approx}$ into two halves over the time axis: the first half of the time frames (indices `0` to `N//2 - 1`) and the second half (`N//2` to `N-1`), where `N` is the total number of frames.
5. For each half, compute the mean magnitude for each frequency bin across its time frames. This gives two 1D arrays of length corresponding to the number of frequency bins.
6. Add `1e-9` to both arrays (for numerical stability) and normalize each so that their elements sum to 1. Treat these as probability distributions $P$ (first half) and $Q$ (second half).
7. Compute the Kullback-Leibler (KL) divergence from $P$ to $Q$ (i.e., $\sum P(i) \log(P(i)/Q(i))$).

Step 2: API Service
Create a web server (e.g., using Flask or FastAPI) listening exactly on `127.0.0.1:8080`.
The API must require an Authorization header for all endpoints: `Authorization: Bearer ds-secret-token-42`. If the token is missing or invalid, return a 401 Unauthorized status.

Implement the following endpoints:
1. `GET /metrics`: Returns a JSON response with the analysis of the audio file:
   ```json
   {
     "singular_value_1": <float>, 
     "kl_divergence": <float>
   }
   ```
   (Where `singular_value_1` is the largest singular value from the SVD of $S$).

2. `POST /compare`: Accepts a JSON payload containing a reference dataset and a test dataset:
   ```json
   {
     "reference": [<list of floats>],
     "test": [<list of floats>]
   }
   ```
   Compute the 1D Wasserstein distance (Earth Mover's Distance) between the `reference` and `test` distributions using `scipy.stats.wasserstein_distance`.
   Return the result as:
   ```json
   {
     "wasserstein_distance": <float>
   }
   ```

Leave the server running in the background or foreground so that it can be tested. Do not write the server to stop after one request.