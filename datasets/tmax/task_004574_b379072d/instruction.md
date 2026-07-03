You are an AI assistant helping a researcher organize and transform a new dataset. The researcher left a recorded audio note containing the specific parameters needed for the feature engineering step. 

Your task involves two main steps:

1. **Information Extraction**:
Analyze the audio file located at `/app/experiment_parameters.wav`. The audio contains spoken digits representing four weight parameters ($w_1$, $w_2$, $w_3$, $w_4$) in order. Extract these four numbers. (You may use Python's built-in tools or any pre-installed system tools to process the audio, but a simple transcription using Python's `speech_recognition` or similar available library is expected).

2. **Feature Engineering Script**:
Create a Python script at `/home/user/process_features.py` that takes a CSV file via standard input and prints the transformed CSV to standard output. 
The input CSV will have four numeric columns: `A`, `B`, `C`, and `D`.
For each row, your script must compute two new features:
- `weighted_sum`: $w_1 \cdot A + w_2 \cdot B + w_3 \cdot C + w_4 \cdot D$
- `interaction`: $(A \cdot B) - (C \cdot D)$

The output must be a standard CSV containing the original columns plus the two new engineered features (`A,B,C,D,weighted_sum,interaction`), retaining the header. Round the new features to exactly 4 decimal places.

Your script must be robust enough to handle any standard CSV formatted this way. Do not print any debug information to standard output; only print the final CSV.