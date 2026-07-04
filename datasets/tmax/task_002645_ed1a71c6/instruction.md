You are an ETL Data Engineer responsible for building an ingest validation pipeline for a machine learning system. 

We have received a configuration audio file from the data science team at `/app/reference_signal.wav`. This audio recording dictates a critical minimum threshold for feature correlation that our models require.

Your task is to write a Python validator script at `/home/user/etl_filter.py` that acts as a strict data filter for incoming JSON files.

**Script Interface:**
The script must accept a single command-line argument (the path to a JSON file) and use exit codes to accept or reject the file:
`python /home/user/etl_filter.py <path_to_json>`
- Exit with code `0` if the JSON is valid (Clean).
- Exit with code `1` if the JSON is invalid (Evil).

**Input Format:**
Each input JSON file contains a single object with a `text` string and a `metrics` array:
```json
{
  "text": "word1 word2 word3",
  "metrics": [
    {"feat_A": 1.2, "feat_B": 1.4, "feat_C": 0.1},
    {"feat_A": 2.1, "feat_B": 2.2, "feat_C": 0.5},
    {"feat_A": 0.5, "feat_B": 0.6, "feat_C": -0.1}
  ]
}
```

**Validation Rules:**
A record is ONLY valid if it passes ALL three of the following tests:
1. **Tokenization & Shape Validation**: When `text` is tokenized by splitting on a single space character (`" "`), the number of text tokens must exactly equal the number of items in the `metrics` array.
2. **Correlation Analysis**: The Pearson correlation coefficient between the sequence of `feat_A` values and `feat_B` values must be strictly greater than the threshold spoken in the `/app/reference_signal.wav` file. (You will need to transcribe this audio file to find the threshold).
3. **Bootstrap Numerical Testing**: Using exactly 1000 bootstrap resamples (with replacement) of the `feat_C` values, calculate the 95% confidence interval of the mean using the percentile method (2.5th and 97.5th percentiles). To pass, the lower bound (2.5th percentile) of this confidence interval must be `>= 0.0`. 
   *(Note: Initialize your random seed to `42` right before the bootstrap loop to ensure deterministic results. Use standard numpy functions for calculating the mean and percentiles).*

You may install any necessary Python packages (like `numpy`, `scipy`, `SpeechRecognition`, `pydub`, `whisper`, etc.) and system dependencies to extract the threshold from the audio and perform the statistical checks.