You are an MLOps engineer tasked with building a reproducible C++ pipeline to analyze a video of a chemical reaction and track experiment artifacts.

We have a video of a chemical reaction changing color over time located at `/app/reaction.mp4`. The color change is highly correlated with the elapsed time (represented by the frame index). 

Your objective is to build an end-to-end data pipeline that extracts the average color of each frame, reduces its dimensionality, and uses linear regression to predict the frame index. You must implement the mathematical and modeling components in a single C++ program.

Here are the exact requirements:

1. **Feature Extraction**:
   - Extract every frame from `/app/reaction.mp4`.
   - Calculate the average Red, Green, and Blue (RGB) values across all pixels for each frame.
   - Save this intermediate data as you see fit.

2. **Dimensionality Reduction & Regression in C++**:
   - Write a C++ program at `/home/user/pipeline.cpp`.
   - The program must read your extracted RGB data.
   - **Standardization**: Standardize the R, G, and B features (subtract the mean and divide by the sample standard deviation, using N-1 for degrees of freedom).
   - **PCA via Power Iteration**: Compute the 3x3 sample covariance matrix of the standardized features. Implement the Power Iteration algorithm to find the dominant eigenvector (the 1st Principal Component). Use at least 100 iterations.
   - **Projection**: Project the 3D standardized RGB features onto this dominant eigenvector to obtain a 1D feature `p` for each frame.
   - **Regression**: Implement Simple Linear Regression from scratch to predict the true frame index ($y$) from the 1D projection ($p$). Fit the model $y = m \cdot p + c$ using the standard least-squares formulas.

3. **Experiment Tracking**:
   - The C++ program must output a reproducible experiment artifact to `/home/user/model_artifacts.json`. It must contain the dominant eigenvector, the slope ($m$), the intercept ($c$), and the Mean Squared Error (MSE) of the predictions on the training data. The exact structure is up to you, but it must be valid JSON.
   - The program must also output the final predictions to `/home/user/predictions.csv`.
   - The CSV must have exactly two columns with the header: `true_index,predicted_index`. The `true_index` should start at 0 for the first frame.

4. **Execution**:
   - Compile your C++ program (you may use `g++` with standard libraries; no external ML libraries like OpenCV or Eigen are allowed for the C++ portion).
   - Run the pipeline to produce `/home/user/predictions.csv` and `/home/user/model_artifacts.json`.

An automated verifier will evaluate the Mean Squared Error (MSE) of your `/home/user/predictions.csv` against the ground truth frame indices. Your model must be highly accurate.