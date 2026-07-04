You are a data analyst tasked with building a content-based recommendation system for a music streaming service. You need to process three CSV datasets to recommend tracks for a specific user (`user_42`).

The datasets are located in `/home/user/data/`:
1. `history.csv`: Contains user listening history (`user_id`, `track_id`, `play_count`).
2. `features.csv`: Contains track audio features (`track_id`, `acousticness`, `danceability`, `energy`, `instrumentalness`, `tempo`).
3. `metadata.csv`: Contains track metadata (`track_id`, `genre`).

You must write a Python script to perform the following steps:
1. **Compute User Profile**: Calculate the profile for `user_42` as the weighted average of the 5 audio features of the tracks they have listened to. The weights are the `play_count` of each track.
2. **Filter Candidates**: Your recommendation candidates must be tracks from the `electronic` genre (found in `metadata.csv`) that `user_42` has **never** listened to.
3. **Dimensionality Reduction**: 
   - Fit a `sklearn.preprocessing.StandardScaler` on the 5 audio features using **all** tracks in `features.csv` (ensure the features are ordered alphabetically: `acousticness`, `danceability`, `energy`, `instrumentalness`, `tempo`).
   - Fit a `sklearn.decomposition.PCA` with `n_components=2` and `random_state=42` on the scaled features of **all** tracks.
4. **Similarity Search**: 
   - Scale and transform both the candidate tracks and the `user_42` profile using the fitted Scaler and PCA models.
   - Calculate the cosine similarity between the 2D PCA vector of `user_42`'s profile and the 2D PCA vectors of the candidate tracks.
5. **Output**: Find the top 3 candidate tracks with the highest cosine similarity. If there is a tie, prioritize the track with the alphabetically earlier `track_id`. Write the result to `/home/user/recommendations.json` in the following exact format:
```json
{
  "user_42": ["track_id_1", "track_id_2", "track_id_3"]
}
```

Make sure to install any necessary Python packages (e.g., `pandas`, `scikit-learn`) using pip.