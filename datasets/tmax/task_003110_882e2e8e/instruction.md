I am building a C-based ETL pipeline that reads video frames, extracts their average brightness as a feature, and uses a simple linear regression model to predict a simulated load metric.

The code is located at `/home/user/pipeline.c`. It reads the video `/app/video.mp4` using `ffmpeg` (via `popen`), computes the frame-by-frame brightness, and performs a 5-fold cross-validation to evaluate the model's Mean Squared Error (MSE). 

Currently, the cross-validated MSE looks suspiciously low. I suspect there is a data leak: the code normalizes the features (Z-score normalization) by computing the mean and standard deviation over the *entire* dataset before performing the train/test splits. This is equivalent to calling `fit_transform` on the whole dataset in scikit-learn before splitting.

Your tasks:
1. Identify and install any missing C dependencies required to compile the GSL-based pipeline (`libgsl-dev` might be needed).
2. Fix the data leak in `/home/user/pipeline.c`. The mean and standard deviation used for normalization must be computed *only* on the training data within each fold of the cross-validation loop. The validation data for that fold should then be scaled using the training mean and standard deviation.
3. Compile your fixed program. E.g., `gcc -O2 pipeline.c -o pipeline -lgsl -lgslcblas -lm`.
4. Run the fixed pipeline. It will print out the corrected cross-validated MSE.
5. Save the final corrected MSE (just the floating point number) into `/home/user/final_mse.txt`.

Ensure your logic correctly avoids any data leakage from the validation folds into the training statistics.