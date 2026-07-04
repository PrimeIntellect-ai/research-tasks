You are an ML engineer tasked with building a reproducible machine learning pipeline to classify audio events. 

You have been provided with a training dataset consisting of a long continuous audio recording located at `/app/train_audio.wav` and an annotations file at `/app/train_labels.csv`. The CSV contains three columns: `start_time` (in seconds), `end_time` (in seconds), and `label` (integer class: 0 or 1). 

Your objective is to:
1. Construct an ETL pipeline that reads the annotations, extracts the corresponding audio segments from the WAV file, and computes robust acoustic features (e.g., Mel-Frequency Cepstral Coefficients - MFCCs) for each segment. 
2. Ensure your numerical and audio processing libraries (like `numpy`, `scipy`, or `librosa`) are correctly configured and installed.
3. Build a reproducible training pipeline that uses these features to train a classifier (e.g., Random Forest, SVM, or Gradient Boosting).
4. Perform cross-validation and hyperparameter tuning to find the optimal model configuration.
5. Save your pipeline and trained model so that it can be applied to new, unlabeled audio files.

Finally, you must write a prediction script at `/home/user/predict.py`. This script must take exactly two command-line arguments:
1. The path to an input WAV file (e.g., `/app/test_audio.wav`)
2. The path to the output CSV file to write predictions to.

The input WAV file for the prediction script will be a continuous recording. We will also provide an evaluation CSV during testing that specifies the segments to predict (using the exact same format as `train_labels.csv`, but without the `label` column). Wait, to make it self-contained for the prediction script, assume the test CSV is always located at `/app/test_segments.csv` when the script is run, and it contains `start_time` and `end_time` columns. Your `predict.py` should read `/app/test_segments.csv`, extract those segments from the provided audio file argument, extract features, run the tuned model, and output the target CSV.

The output CSV must contain a single column `prediction` with the predicted integer labels (0 or 1) in the exact same order as the segments in `/app/test_segments.csv`. No header is necessary, just the predicted integers, one per line.

Requirements:
- Use Python as the primary language.
- The entire process must be scriptable and reproducible. 
- You must achieve a reasonable classification performance (we will test your `predict.py` on a hidden test audio file and evaluate the accuracy/F1 score).