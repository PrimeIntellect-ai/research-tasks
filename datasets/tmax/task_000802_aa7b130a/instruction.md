You are an AI assistant acting as a Data Scientist. We have an unusual dataset split across a CSV file and a video file.

Files provided in `/app/`:
- `/app/texts.csv`: Contains 1,000 text reviews (one per line, no header).
- `/app/labels.mp4`: A video file containing the labels for the reviews. The video has exactly 1,000 frames (10 FPS, 100 seconds). Frame index `i` corresponds to row `i` in `texts.csv`. If the frame is predominantly GREEN, the label is 1 (positive). If the frame is predominantly RED, the label is 0 (negative).
- `/app/plot_results.py`: A script intended to plot your hyperparameter tuning results. However, it currently outputs a completely blank image due to a matplotlib backend misconfiguration.

Your task:
1. **Environment Setup**: Install any necessary packages (e.g., `opencv-python`, `scikit-learn`, `pandas`, `matplotlib`).
2. **Dataset Preparation**: 
   - Extract the frames from `/app/labels.mp4`.
   - Determine the color of each frame to extract the binary labels (0 or 1).
   - Combine these labels with the texts from `/app/texts.csv`.
3. **Tokenization & Modeling**:
   - Tokenize the text data.
   - Use cross-validation and hyperparameter tuning to train a text classification model (e.g., Logistic Regression or SVM) to predict the label from the text.
   - Save your trained model pipeline (which should include both the vectorizer and the classifier) to `/home/user/best_model.pkl` using `joblib`.
4. **Fix the Plot**:
   - Fix `/app/plot_results.py` so that it correctly saves the plot instead of a blank image. (Hint: look into matplotlib backends). Run it to produce `/home/user/cv_results.png`.

Your model will be evaluated on a hidden test set. It must achieve an accuracy of at least 0.85.