You are an MLOps engineer tasked with recovering an experiment artifact. A critical sensor recording, located at `/app/sensor_data.wav`, has been corrupted with severe background noise. 

You must build a tabular data pipeline in Python to denoise this audio artifact using dimensionality reduction.

Here are the specific steps you must implement:
1. **Feature Extraction:** Load the audio file using `librosa` or `scipy`. Compute the Short-Time Fourier Transform (STFT). Separate the magnitude and phase.
2. **Tabular Transformation:** Convert the magnitude matrix into a pandas DataFrame where each column is a frequency bin and each row is a time frame. 
3. **Data Schema Enforcement:** You have been provided a metadata file at `/app/frame_metadata.csv` containing labels for *some* of the frames. Merge your STFT DataFrame with this metadata on the frame index (`frame_id`). 
   *Crucial:* Because the metadata is incomplete, merging will introduce `NaN` values, which inherently causes pandas to silently convert the integer `frame_id` to floats. You must strictly enforce the schema: the `frame_id` column must remain an exact integer type (e.g., using pandas' nullable integer data type `Int64` or by appropriately filling missing values), and no rows should be dropped. 
4. **Dimensionality Reduction:** Apply Principal Component Analysis (PCA) to the magnitude features, retaining only the top 2 principal components. Inverse-transform the PCA to get a smoothed, denoised magnitude matrix.
5. **Reconstruction:** Combine the denoised magnitude with the original phase and perform an Inverse STFT (ISTFT) to reconstruct the audio signal.
6. **Artifact Tracking:** Save the resulting denoised audio to `/home/user/recovered_sensor.wav` using the same sample rate as the original file.

You are free to use any standard bash commands and write Python scripts to accomplish this. Make sure you install any necessary Python packages (e.g., `librosa`, `scipy`, `scikit-learn`, `pandas`).