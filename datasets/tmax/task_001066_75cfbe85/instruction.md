You are a Machine Learning Engineer preparing training data for an audio analysis model. Your task is to extract acoustic features, perform feature selection, and create a bootstrapped dataset from a provided raw audio recording.

An audio file is located at `/app/input_audio.wav` (which is a 16kHz, mono WAV file). 

Perform the following steps using Python:

1. **Environment Setup**: Ensure you have necessary numerical and audio libraries installed (e.g., `librosa`, `numpy`, `scipy`).
2. **Feature Extraction**: Process the audio in non-overlapping 20ms frames (320 samples per frame). For each frame, extract exactly 15 features using `librosa` with the following strict configurations (`center=False` for all):
   - **RMS Energy**: 1 feature. (`frame_length=320`, `hop_length=320`)
   - **Zero-Crossing Rate (ZCR)**: 1 feature. (`frame_length=320`, `hop_length=320`)
   - **MFCCs**: 13 features (MFCC 1 to 13). (`sr=16000`, `n_mfcc=13`, `n_fft=320`, `hop_length=320`, `n_mels=40`). 
   *Note: Concatenate these to form a feature vector of length 15 for each frame. The order of your 15 features before selection should be: [RMS, ZCR, MFCC_1, MFCC_2, ..., MFCC_13].*
3. **Feature Selection**: Calculate the variance of each of the 15 features across all frames in the audio file. Identify and select the top 4 features with the highest variance.
4. **Filtering**: Filter the frames, retaining ONLY the frames where the RMS Energy is strictly greater than the median RMS Energy of ALL frames. 
5. **Bootstrapping**: To create a robust representative set, use NumPy to randomly sample exactly 10,000 frames with replacement from your filtered frames. 
   - **Important**: Set the random seed using `numpy.random.seed(42)` immediately before calling the sampling function (e.g., `np.random.choice`).
6. **Output**: Save the bootstrapped dataset (only the 4 selected features) to `/home/user/prepared_features.csv`. The file must contain exactly 10,000 rows and 4 columns, separated by commas, with no header row and no index column.

Ensure your script is efficient and outputs the exact requested format. Your result will be evaluated automatically by comparing the statistical distribution (column means) of your generated CSV against the expected reference distribution.