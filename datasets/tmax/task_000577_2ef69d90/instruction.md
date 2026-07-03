You are tasked with analyzing a biological sequence transmitted from a legacy lab instrument via an audio signal. 

The lab encoded a DNA sequence into DTMF (Dual-Tone Multi-Frequency) tones and recorded it to `/app/dna_telemetry.wav`. 
The mapping of keypad numbers to DNA bases is:
- '2' -> A
- '3' -> C
- '4' -> G
- '5' -> T

Standard DTMF frequencies apply:
- '2': 697 Hz + 1336 Hz
- '3': 697 Hz + 1477 Hz
- '4': 770 Hz + 1209 Hz
- '5': 770 Hz + 1336 Hz

Each tone in the audio file lasts approximately 0.4 seconds, separated by 0.1 second of silence. 

Your objectives are:
1. **Signal Decoding**: Write a Python script to process the audio file, identify the DTMF tones, and reconstruct the full DNA sequence (e.g., "ACCGT...").
2. **Markov Chain Analysis**: Treat the sequence as a first-order Markov chain. Calculate the 4x4 empirical transition probability matrix $P$.
3. **Stationary Distribution**: Using matrix decomposition or linear equation solving, compute the stationary distribution $\pi$ of this Markov chain (where $\pi = \pi P$ and $\sum \pi_i = 1$).
4. **Statistical Hypothesis Comparison**: Perform a Chi-squared goodness-of-fit test on the transition counts to compare the observed transitions against the null hypothesis that all transitions from a given state are equally likely (i.e., uniform transition probabilities of 0.25).
5. **API Service**: Set up and run an HTTP server listening on `127.0.0.1:8000`. It must expose a single `GET /results` endpoint that returns a JSON object with the following schema:
   ```json
   {
     "sequence": "<decoded DNA string>",
     "stationary_distribution": {
       "A": <float>,
       "C": <float>,
       "G": <float>,
       "T": <float>
     },
     "p_value": <float>
   }
   ```

Ensure your Python environment is properly managed and install any necessary scientific packages (e.g., `scipy`, `numpy`, `flask` or `fastapi`). Keep the service running so the automated verifier can query your endpoint.