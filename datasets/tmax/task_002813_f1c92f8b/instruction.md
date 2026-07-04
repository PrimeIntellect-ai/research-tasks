You are a data analyst at a marketing firm. We have received a new dataset of user engagement metrics, along with an audio memo from the client detailing their specific targeting request for an upcoming campaign.

Your objectives:
1. **Understand the Request:** Listen to (or transcribe) the client's audio memo located at `/app/audio/client_request.wav`. It contains instructions on which features to ignore and the specific "Target User ID" they want to base their campaign on.
2. **Data Cleaning & Feature Engineering:** Load the dataset at `/app/data/user_engagement.csv`. Drop the columns specified in the audio memo. Standardize the remaining feature columns (mean=0, variance=1).
3. **Dimensionality Reduction:** Apply Principal Component Analysis (PCA) to reduce the standardized features to exactly 10 principal components.
4. **Similarity Search:** Using the 10-dimensional PCA space, compute the Cosine Similarity between the "Target User" and all other users. Find the top 100 most similar users (excluding the target user themselves).
5. **Output Generation:** Save these top 100 users to `/home/user/top_100_similar.csv`. The CSV must contain exactly two columns: `user_id` and `similarity_score`, sorted in descending order of similarity.
6. **Fix the Visualization:** The client also provided a script at `/app/scripts/generate_plot.py` intended to visualize the 2D PCA projection of the dataset. However, due to a misconfiguration in how the plot is rendered and saved, the script currently produces a completely blank image at `/home/user/pca_plot.png`. Debug and fix `/app/scripts/generate_plot.py` so that it successfully saves the actual scatter plot without relying on a GUI backend (as you are in a headless environment).

Ensure your final similarities are accurate, as your results will be graded on a Recall@100 metric against the canonical solution.