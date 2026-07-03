You are an AI assistant helping a data analyst build an automated data filtering pipeline. 

We have a reference audio file at `/app/reference_report.wav` containing a spoken medical observation. 
We also have a collection of CSV logs containing transcribed reports. Some of these reports are relevant to the reference audio (clean), while others are irrelevant or adversarial noise (evil).

Your task is to create a Python script at `/home/user/filter_transcripts.py` that processes a given input CSV and outputs a filtered CSV containing only the relevant rows.

The script must conform to this CLI signature:
`python /home/user/filter_transcripts.py --input <input_csv_path> --output <output_csv_path>`

Requirements for the script:
1. **Audio Transcription**: Transcribe the audio file at `/app/reference_report.wav` to text (you may use the `openai-whisper` library).
2. **Embedding Computation**: Use the `sentence-transformers` library (model: `all-MiniLM-L6-v2`) to compute embeddings for the reference transcription and the text in the `transcript` column of the input CSV.
3. **Correlation Analysis**: Compute the cosine similarity (correlation) between the reference embedding and each row's embedding. 
4. **Filtering**: Retain only rows that are semantically related to the reference audio. Choose an appropriate similarity threshold (e.g., 0.4) to classify rows as valid.
5. **Experiment Tracking**: After processing each file, append a JSON object to `/home/user/experiment_log.jsonl` tracking the run:
   `{"input_file": "<input_csv_path>", "accepted": <int>, "rejected": <int>}`

We have provided a sample dataset for you to calibrate your script:
- `/app/corpus/clean/`: Contains CSV files with valid, related medical transcripts.
- `/app/corpus/evil/`: Contains CSV files with unrelated, anomalous transcripts.

Your script will be verified against a hidden validation set using the exact CLI signature above. To pass, your script must preserve 100% of the rows in the clean validation CSVs and reject 100% of the rows in the evil validation CSVs.

Note: You can install necessary packages using `pip`.