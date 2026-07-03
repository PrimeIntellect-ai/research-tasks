You are assisting a machine learning researcher in organizing an audio dataset. They have been extracting features from audio files and combining them with tabular metadata, but they noticed their model evaluation is overly optimistic due to a data leakage bug in their preprocessing pipeline (specifically, test data statistical properties are leaking into the training set during feature scaling).

Your task is to write a robust Python script `/home/user/pipeline.py` that properly extracts audio features, merges them with tabular data, and scales the features without leaking test set statistics.

Requirements for `/home/user/pipeline.py`:
1. **Command Line Arguments:** The script must accept exactly two positional arguments: `<input_csv>` and `<output_csv>`.
2. **Input Format:** The input CSV will contain the following columns: `id` (integer), `split` (string, either "train" or "test"), `audio_path` (string, absolute path to a WAV file), `f1` (float), and `f2` (float).
3. **Audio Processing:**
   - For each row, load the audio file using `librosa.load(path, sr=22050)`.
   - Extract exactly 5 MFCCs using `librosa.feature.mfcc(y=y, sr=22050, n_mfcc=5, n_fft=2048, hop_length=512)`.
   - Calculate the mean of each of the 5 MFCCs across the time axis (resulting in 5 float values: `mfcc0` to `mfcc4`).
4. **Data Scaling (The Leakage Fix):**
   - Concatenate the tabular and audio features into a 7-dimensional vector for each row: `[f1, f2, mfcc0, mfcc1, mfcc2, mfcc3, mfcc4]`.
   - Use `sklearn.preprocessing.StandardScaler` to standardize these features.
   - **Crucial:** To fix the data leakage, the scaler must be `.fit()` **ONLY** on the subset of data where `split == 'train'`.
   - Apply the `.transform()` operation to all rows (both "train" and "test" splits) using this fitted scaler.
5. **Output Format:**
   - Save the processed data to the specified `<output_csv>`.
   - The output CSV must have the following columns in exact order: `id,split,f1,f2,mfcc0,mfcc1,mfcc2,mfcc3,mfcc4`.
   - Sort the output rows by `id` in ascending numerical order.
   - All float values in the output CSV must be formatted to exactly 4 decimal places (e.g., `1.2340`, `-0.0001`).

You have been provided a sample audio file at `/app/sample.wav` which you can use to locally test your script by manually creating a small dummy CSV. 

Ensure your environment has the necessary libraries (e.g., `pip install librosa pandas scikit-learn numpy`) before testing. Your final solution will be rigorously tested against an automated fuzzer that will verify your script produces bit-exact outputs identical to a reference oracle.