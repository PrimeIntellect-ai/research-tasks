You are a data scientist troubleshooting a Non-negative Matrix Factorization (NMF) pipeline used for acoustic analysis. The model frequently crashes with numerical instability when fitting to certain spectral feature matrices. You suspect the issue is caused by near-singular inputs (matrices with high condition numbers) in the dataset.

Your colleague left a voicemail with the exact numerical threshold they established for acceptable matrix condition numbers, but they have since gone on vacation.

Here is what you need to do:
1. First, process the voicemail located at `/app/audio/voicemail.wav`. You will need to transcribe it to recover the exact threshold condition number. You may use any available Python library (e.g., `scipy`, `SpeechRecognition`, or a local `whisper` setup if available, though standard API calls to free transcription services or local analysis is up to you).
2. Write a Python sanitisation script at `/home/user/sanitiser.py`.
3. The script must take an input directory of 2D NumPy array files (`.npy`) and an output JSON file path.
   Usage must be: `python /home/user/sanitiser.py --input_dir <path> --output_file <path>`
4. The script should load each `.npy` file in the directory, calculate its condition number (using L2 norm), and classify it based on the threshold spoken in the voicemail.
5. The output JSON must have the following exact structure:
```json
{
    "file1.npy": "clean",
    "file2.npy": "evil",
    ...
}
```
"clean" means the condition number is strictly less than the threshold.
"evil" means the condition number is equal to or greater than the threshold (these are the near-singular inputs causing the crashes).

Ensure your script handles exceptions gracefully and only outputs the JSON dictionary mapping the base filename (e.g., "matrix_001.npy") to its classification string.