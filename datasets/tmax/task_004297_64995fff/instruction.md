You are helping prepare an automated training data pipeline for a novel protein sequence generation model. One of our researchers dictated a short protein sequence into an audio file, and we need to verify how closely the amino acid distribution of this dictated sequence matches our reference dataset.

Here is what you need to do:
1. We have an audio recording of a researcher dictating a sequence of single-letter amino acid codes (e.g., "M", "A", "C") at `/app/dictation.wav`. Transcribe this audio to recover the sequence.
2. We have a reference sequence in a FASTA file located at `/app/reference.fasta`. Parse this file to get the reference protein sequence.
3. Calculate the amino acid frequency distribution (normalized probabilities for each of the 20 standard amino acids) for both the transcribed sequence and the reference sequence.
4. Compute the Wasserstein distance (Earth Mover's Distance) between these two probability distributions (using an alphabetical ordering of the 20 standard amino acid codes as the coordinate space, i.e., A=0, C=1, D=2, ..., Y=19).
5. Start a background Python HTTP server listening on `127.0.0.1:9090`. 
6. The server must expose a `GET /metrics` endpoint that returns a JSON response containing the transcribed sequence and the computed distance, matching exactly this format:
   ```json
   {
     "transcription": "MAC...",
     "wasserstein_distance": 1.05
   }
   ```

Write the necessary Python script(s) to perform the transcription, calculation, and server hosting. You may use `ffmpeg`, `whisper` (if installed), or any standard Python scientific libraries (`scipy`, `numpy`, `biopython`). Leave the server running in the background.