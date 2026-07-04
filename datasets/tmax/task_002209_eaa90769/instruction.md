You are an ML Engineer preparing an ETL and dimensionality reduction pipeline for text data. We have an audio recording of a meeting where the Chief Data Scientist specified the exact pipeline hyperparameters, but the original notes were lost.

First, you must transcribe the audio file located at `/app/audio/hparams_meeting.wav` to recover the pipeline configuration. You can use any available tool (e.g., installing `openai-whisper` or using `ffmpeg` + other tools). 

Next, based on the hyperparameters mentioned in the audio, write a Python script at `/home/user/etl.py` that performs feature engineering and dimensionality reduction exactly as specified below.

The script must accept a single command-line argument: the path to a JSON file containing a list of strings.
Usage: `python /home/user/etl.py input_data.json`

Your script must implement the following pipeline strictly:
1. Load the JSON list of strings.
2. For each string, compute the character-level bigram frequencies (counts) strictly for lowercase letters `a` through `z`. Ignore all punctuation, numbers, and spaces. For example, the string "a b c! ab" yields bigrams `ab`, `bc`, `ca`, `ab` if spaces/punctuation are removed to form "abcab". So `ab`:2, `bc`:1, `ca`:1. 
3. Create a feature matrix of size `N x 676`, where N is the number of strings, and the columns represent all possible a-z bigrams in lexicographical order ('aa', 'ab', ..., 'zz').
4. Fit and transform the feature matrix using `sklearn.preprocessing.StandardScaler` (with default parameters).
5. Fit and transform the scaled matrix using `sklearn.decomposition.PCA`. Use the number of components (`n_components`) and the `random_state` specified in the audio file.
6. Print the resulting transformed matrix to standard output (stdout) as a CSV, with exactly 4 decimal places of precision, with no header and no index. Values should be comma-separated.

Example output format for N=2 and components=3:
```
-1.0421,0.5012,-0.1102
1.0421,-0.5012,0.1102
```

Your script will be tested against a reference implementation using an automated fuzzer that will supply hundreds of randomly generated JSON lists of strings to verify exact bit-for-bit equivalence. Ensure your logic is perfectly deterministic and matches the specification.