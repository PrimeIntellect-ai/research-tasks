Hello, our data science team has been struggling with a data leakage issue in our scikit-learn preprocessing pipelines. We recently had a meeting where the lead data scientist outlined a specific, custom algorithm to fix this leakage during our feature engineering step. 

The recording of this specification has been provided to you at `/app/instructions.wav`. 

Your task is to:
1. Extract the instructions from the audio file.
2. Implement the exact preprocessing and data cleaning algorithm described in the recording.
3. Save your solution as a Python script at `/home/user/transform.py`.

Your script will be tested against a rigorous automated fuzzer to ensure it is perfectly equivalent to the lead data scientist's reference implementation. 

**Script Interface Requirements:**
- The script must be executable via: `python3 /home/user/transform.py <N>`
- `<N>` is an integer representing the size of the training split (the first N rows).
- The script must read input from standard input (`stdin`). The input will be a newline-separated list of floating-point numbers.
- The script must output the cleaned and transformed dataset to standard output (`stdout`), printing each transformed floating-point number on a new line, formatted to exactly 4 decimal places.

Make sure to carefully handle missing values, outliers, and scaling exactly as specified in the audio to prevent data leakage from the test set (rows after `N`) into the training statistics.