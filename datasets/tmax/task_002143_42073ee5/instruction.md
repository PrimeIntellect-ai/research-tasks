You are a Machine Learning Engineer preparing a dataset of spoken digits for an audio classification model. You've discovered that several batches of your training data have been corrupted by a strange continuous-wave interference pattern. 

Because the interference has a stable, repeating spectral signature, it appears as a highly structured, low-rank component in the Time-Frequency domain (Spectrogram). In contrast, the spoken digits act as a sparse component.

To clean your training pipeline, you need to build a detector that can automatically flag corrupted audio files so they can be discarded. 

Your task is to write a command-line tool `/home/user/detector.py` that does the following for a given directory of `.wav` files:
1. Loads each audio file and computes its Short-Time Fourier Transform (STFT) magnitude spectrogram (using standard spectroscopy/signal processing techniques).
2. Uses an iterative matrix decomposition algorithm (such as Robust Principal Component Analysis via Inexact Augmented Lagrange Multipliers or Alternating Direction Method of Multipliers) to separate the magnitude spectrogram into a Low-Rank matrix (the interference) and a Sparse matrix (the speech).
3. The iterative decomposition must use Singular Value Decomposition (SVD) at each step and must implement a strict convergence test (e.g., the Frobenius norm of the reconstruction error drops below a threshold like `1e-5`).
4. Calculates the energy (sum of squared elements) of the Low-Rank component and the total energy of the original magnitude spectrogram. 
5. If the Low-Rank energy is greater than 15% of the total energy, classify the file as `"corrupted"`. Otherwise, classify it as `"clean"`.

I have provided a sample corrupted audio file at `/app/sample_interference.wav` so you can analyze the signal and test your STFT and matrix decomposition implementations. 

Your script must expose the following CLI interface:
`python3 /home/user/detector.py --input <directory_path> --output <json_file_path>`

The output JSON must be a single dictionary mapping the base filename (e.g., `audio_01.wav`) to its classification string (`"clean"` or `"corrupted"`).

Ensure your script is robust and uses standard scientific computing libraries (like `numpy`, `scipy`, or `librosa`).