You are a data scientist tasked with cleaning a 2D sensor dataset using a custom C program. The dataset contains 1000 noisy readings, and due to a misconfiguration in the data pipeline, some readings are extreme anomalies. 

You need to write a C program at `/home/user/clean_points.c` that processes `/home/user/points.csv` and filters out the anomalies based on spatial similarity and probabilistic bounds.

The file `/home/user/points.csv` contains comma-separated `x,y` coordinates (floats) on each line.

Your C program must perform the following steps exactly:
1. Read all points from `/home/user/points.csv`.
2. Compute the centroid (mean of X, mean of Y) of all points.
3. For each point, calculate its Euclidean distance to the centroid ($d_i$).
4. Compute the mean ($\mu_d$) and the population standard deviation ($\sigma_d$) of these distances.
5. Identify a point as an outlier if its distance to the centroid satisfies $d_i > \mu_d + 2.0 \times \sigma_d$.
6. Write all non-outlier points (in their original order) to `/home/user/cleaned_points.csv`, formatting each line exactly as `%.6f,%.6f\n`.
7. Write the total count of removed outliers (as a simple integer) to `/home/user/outlier_count.txt`.

Compile and run your C program so that the output files are generated. Do not use external libraries other than the standard C library (and math library `-lm`).