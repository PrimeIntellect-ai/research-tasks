You are an AI assistant helping a data scientist fix an audio processing pipeline and deploy an inference script. We are filtering customer support voice recordings to detect "adversarial" prompt injections (users trying to hack our automated voice system).

Your task has three parts:

1. **Fix the Data Leak & Train the Model**
You will find a workspace at `/home/user/workspace/`. Inside, `train.py` trains a Logistic Regression model on TF-IDF features to classify transcripts as 'clean' (0) or 'evil' (1). It uses Principal Component Analysis (PCA) for dimensionality reduction. However, there is a data leak: PCA is currently being fit on the entire dataset *before* the train/test split!
- Fix `train.py` to properly split the data first, then fit PCA only on the training set, and apply the transformation to both sets.
- Train the model and save the `vectorizer`, `pca_model`, and `classifier` as `.pkl` files in `/home/user/workspace/models/`.
- Ensure your model output validation shows accurate results on the test set.

2. **Benchmark & Transcribe the Sample Audio**
We have a sample audio file located at `/app/sample_audio.wav`. 
- Install necessary tools (e.g., `openai-whisper`, `ffmpeg`).
- Transcribe `/app/sample_audio.wav`.
- Run your fixed dimensionality reduction and model inference on this transcript to classify it.
- Write a benchmarking script `benchmark.py` that measures the inference time for 100 iterations of your feature-extraction + PCA + classification pipeline on this transcript. Output the average inference time to `/home/user/workspace/benchmark.log`.

3. **Create the Adversarial Detector**
Create a script `/home/user/workspace/detector.py` that acts as the final inference entry point. 
It must accept a single command-line argument (the path to a `.wav` file):
`python /home/user/workspace/detector.py <path_to_wav>`
The script should:
- Transcribe the audio.
- Transform the text using your saved vectorizer.
- Apply the saved PCA (dimensionality reduction).
- Run the classifier.
- Print exactly `CLEAN` to standard output if the class is 0, or `EVIL` if the class is 1.

The automated verification system will run your `detector.py` against a hidden adversarial corpus of audio files. Your detector must correctly identify the malicious audio files while preserving the clean ones.