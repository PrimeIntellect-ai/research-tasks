I am trying to run a simple data science pipeline to find similar movies based on their descriptions. I have a script located at `/home/user/generate_report.py` and a dataset at `/home/user/movies.csv`.

However, the script is broken and failing for a few reasons:
1. I am running this in a headless Linux environment, and the plotting library seems to be misconfigured or crashing when trying to create a window.
2. The dataset has some missing values in the `description` column, which is causing the text vectorizer to crash.
3. The script is supposed to find the top 3 most similar pairs of movies, but it currently includes movies being similar to themselves (a similarity of 1.0).

Please fix the script `/home/user/generate_report.py` so that it successfully executes.
You will need to:
- Install any missing dependencies (the script uses `pandas`, `scikit-learn`, `matplotlib`, and `seaborn`).
- Fix the script so it handles missing values in the `description` column by replacing them with empty strings.
- Configure matplotlib correctly so it generates the plot without attempting to open a graphical window.
- Fix the logic to extract the top 3 *distinct* pairs of movies (exclude pairs where movie A is the same as movie B, and avoid duplicates like [A, B] and [B, A] by only keeping one).
- Save the top 3 pairs to `/home/user/top_pairs.json` in the exact format: `[["Movie Title 1", "Movie Title 2", 0.95], ["Title 3", "Title 4", 0.82], ["Title 5", "Title 6", 0.75]]` (sorted by similarity descending). Round the similarity score to 3 decimal places.
- Ensure the script successfully saves `/home/user/heatmap.png`.

Run the script and make sure the outputs are generated correctly.