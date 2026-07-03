Hello! I am a researcher organizing and analyzing my datasets. I wrote a Python script to perform dimensionality reduction, train a classifier, and estimate its accuracy using bootstrap sampling. However, I've run into a few issues and need your help to fix them.

My workspace is located at `/home/user/workspace/` and my dataset is at `/home/user/data/dataset.csv`. The script I am working on is `/home/user/workspace/analyze_data.py`.

Here are the problems I need you to solve:
1. **Headless Plotting Error**: When I run the script on my remote Linux server, it crashes or produces blank plots because of the matplotlib backend. Please configure matplotlib within the script to use a backend suitable for headless environments (like 'Agg') so it successfully saves `/home/user/workspace/pca_plot.png`.
2. **Missing Dimensionality Reduction**: I left a `TODO` in the script. The features `X` need to be reduced to exactly 2 dimensions using Principal Component Analysis (PCA) before plotting and training.
3. **Bootstrap Sampling Bug**: In my bootstrap loop, I am using `np.random.choice` but I accidentally set it to sample *without* replacement. Bootstrap sampling requires sampling *with* replacement. Please fix this.
4. **Confidence Interval Calculation**: I am trying to calculate the 95% confidence interval for the accuracy, but I used the 10th and 90th percentiles. Please correct this to use the proper percentiles for a 95% confidence interval (2.5th and 97.5th).

Please modify `/home/user/workspace/analyze_data.py` to fix these 4 issues, and then execute the script so that it generates both `/home/user/workspace/pca_plot.png` and `/home/user/workspace/metrics.txt`. Do not change the random seeds or the number of iterations already defined in the script.

Let me know when the files are generated!