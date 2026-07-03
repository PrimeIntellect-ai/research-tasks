You are assisting a researcher in organizing and modeling a multimodal dataset. The dataset includes tabular sensor measurements with severe data quality issues and an audio recording of a researcher dictating missing feature values.

Your objective is to build a robust pipeline that cleans the data, enforces schema consistency, extracts features from audio, and trains a predictive model.

Here are your resources:
1. Tabular Data:
   - `/app/data/train.csv`: Training dataset with columns `id`, `feature_A`, `feature_B`, and `target`. This file contains missing values and extreme outliers.
   - `/app/data/test.csv`: Test dataset with columns `id`, `feature_A`, `feature_B`, and `feature_C`.

2. Audio Data:
   - `/app/audio/dictation.wav`: An audio recording of the researcher speaking the numeric values for a missing feature, `feature_C`, for the training set. The values are dictated in sequential order matching the `id` column of `train.csv` (e.g., "five point two", "negative three", etc.). There is exactly one dictated number per row in the original `train.csv`.

Pipeline Requirements:
1. Environment Setup: Install any necessary Python libraries (e.g., `SpeechRecognition`, `pydub`, `scikit-learn`, `pandas`, `scipy`) to process the audio and tabular data.
2. Audio Extraction: Transcribe `/app/audio/dictation.wav` and parse the spoken numbers into a list of numerical values. Map these values as the `feature_C` column to the corresponding `id`s in `train.csv`.
3. Data Cleaning & Schema Enforcement:
   - Impute missing values (NaNs) in `feature_A` and `feature_B` using the median of their respective columns.
   - Detect and remove outliers in `feature_A` and `feature_B` from the training set. An outlier is defined as any value with a Z-score strictly greater than 3.0 or less than -3.0 (compute Z-scores on the imputed data).
   - Ensure all features (`feature_A`, `feature_B`, `feature_C`) and the `target` are standard floats.
4. Modeling: Train a `RandomForestRegressor` (with `n_estimators=100` and `random_state=42`) using `feature_A`, `feature_B`, and `feature_C` to predict the `target` on your cleaned training data.
5. Inference: Process `/app/data/test.csv` using the same imputation statistics (medians) derived from the training set. The test set already contains `feature_C`, so no audio extraction is needed for it. Generate predictions for the test set.

Output:
Save your final test set predictions to `/home/user/predictions.csv`. The file must contain exactly two columns: `id` and `prediction`.

The quality of your pipeline will be evaluated by an automated script that calculates the Mean Absolute Error (MAE) of your predictions against a hidden ground-truth file. You must achieve an MAE of less than 2.5 to succeed.