You are tasked with fixing a critical issue in our audio processing ETL pipeline. Our pipeline expects integer outputs from a downstream feature quantization step, but occasionally, an anomalous audio file causes our pandas-based transformation step to silently introduce NaNs. This casts our integer columns to floats, breaking the downstream database schema.

To prevent these files from entering the pipeline, you need to build a data sanitizer. 

First, listen to the system architect's mission brief located at `/app/brief.wav`. You will need to transcribe this audio file to obtain the exact parameters and thresholds required for the anomaly detection algorithm.

Once you have the parameters, create a script at `/home/user/sanitizer.py` that determines whether an audio file is "clean" (safe for the pipeline) or "evil" (will cause the NaN/float conversion).

Your script must implement the exact dimensionality reduction check requested by the architect. The general procedure is:
1. Load the target audio file using `librosa` (default sampling rate).
2. Extract the MFCCs (default librosa parameters).
3. Transpose the MFCC matrix so that rows correspond to time frames and columns correspond to MFCC coefficients.
4. Standardize the features (zero mean, unit variance per coefficient).
5. Apply Principal Component Analysis (PCA). 
6. Check the variance condition specified in the audio brief.

Your script will be invoked as follows:
`python /home/user/sanitizer.py <path_to_audio_file.wav>`

Requirements:
- If the file is "clean" (meets the condition), the script MUST exit with code `0`.
- If the file is "evil" (violates the condition), the script MUST exit with code `1`.
- You may install any necessary numerical libraries, audio processing tools, and speech-to-text tools (like `openai-whisper` or `SpeechRecognition`) to complete this task.
- The script must be completely self-contained and run unattended.