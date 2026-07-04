You are a machine learning engineer preparing training data for a bioinformatics model predicting primer binding efficiency. You have inherited a partially completed project. 

Your tasks:

1. **Audio Transcription**: 
   Listen to or process the audio file located at `/app/sequence_audio.wav`. It contains a researcher dictating a target reference DNA sequence. Extract the sequence (consisting only of the letters A, T, G, C; ignore any spaces or punctuation).

2. **Custom Scoring Implementation**:
   We have a proprietary compiled binary `/app/bin/oracle_score` that computes a custom primer-alignment score between two sequences. We need a reproducible Python version of this. 
   Write a Python script at `/home/user/score.py` that accepts exactly two positional arguments (Sequence 1 and Sequence 2) and prints only the final integer score to standard output.
   
   The scoring algorithm works as follows:
   - Extract all overlapping 3-mers (substrings of length 3) from Sequence 1.
   - For each 3-mer extracted from Sequence 1, if it exists as a substring anywhere in Sequence 2, add 3 to the total score. (If a 3-mer appears multiple times in Sequence 1, each instance is evaluated and scored independently).
   - Finally, subtract the absolute difference in length between Sequence 1 and Sequence 2 from the score.
   
   Your `/home/user/score.py` must perfectly match the behavior of `/app/bin/oracle_score` for any combination of ATGC sequences.

3. **Data Reshaping Pipeline**:
   You are provided with observational data in `/app/patient_reads.csv` with columns: `sample_id`, `read_id`, `sequence`.
   Write a reproducible bash script `/home/user/process_data.sh` that:
   - Uses your `/home/user/score.py` to calculate the score between the reference sequence (from the audio) as Sequence 1, and the `sequence` from the CSV as Sequence 2.
   - Reshapes the scored data into a feature matrix where rows are `sample_id` and columns are `read_id`s (e.g., 'R1', 'R2').
   - The values in the matrix should be the calculated scores. If a sample lacks a particular read_id, fill the missing value with 0.
   - Saves the final reshaped matrix as a comma-separated file to `/home/user/features.csv`, sorted by `sample_id`.

Ensure your python script and bash pipeline are robust. You can install any required python packages (like `SpeechRecognition` or `pydub` or `pandas`) using standard package managers.