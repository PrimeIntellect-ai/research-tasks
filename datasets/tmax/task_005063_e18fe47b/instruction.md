You are an MLOps engineer responsible for a pipeline that detects corrupted (or "evil") video feeds based on frame-level statistics. 

You have been provided with:
1. `/home/user/train_data.csv`: A dataset containing historical frame features (`brightness`, `contrast`, `sharpness`, `motion_corr`) and a `label` (0 for clean, 1 for evil).
2. `/home/user/train.py`: A draft training script that trains a Logistic Regression model using PCA for dimensionality reduction.
3. `/home/user/extract.py`: A utility script that takes an MP4 video file and extracts frame features to a CSV.
4. `/app/test_video.mp4`: A newly ingested video file that needs to be analyzed.

Unfortunately, `train.py` contains a critical MLOps anti-pattern: a data leak where `PCA.fit_transform` is applied to the entire dataset *before* `train_test_split`, artificially inflating validation metrics.

Your tasks are:
1. **Fix and Train**: Modify `/home/user/train.py` to fix the data leakage by incorporating PCA correctly into a `scikit-learn` Pipeline so that it fits only on the training split. Compute the 95% confidence interval of the model's accuracy on the test set (using a normal approximation) and print it. Save the trained pipeline to `/home/user/model.pkl`.
2. **Create Detector**: Write a script `/home/user/detector.py` that takes a single argument (the path to a CSV file containing frame features without labels), loads `/home/user/model.pkl`, and predicts the overall video label. If the average prediction probability for class 1 across all frames is > 0.5, the script must print exactly `EVIL` to standard output. Otherwise, it must print exactly `CLEAN`.
3. **Analyze Video**: Use `/home/user/extract.py` to extract features from `/app/test_video.mp4` into `/home/user/video_features.csv`. Then run your detector on this CSV and redirect the output to `/home/user/video_result.txt`.

Ensure your model generalizes well, as your `detector.py` will be rigorously evaluated against a hidden adversarial corpus of clean and evil feature CSVs.