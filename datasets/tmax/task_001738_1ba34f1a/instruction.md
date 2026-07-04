You are acting as a data scientist fitting spatial probability models. We have a dataset of spatial events and need to compare their empirical spatial distribution against an analytical theoretical model using an adaptive mesh.

Your task is to write a C++ program that performs domain decomposition, computes an empirical distribution, validates it against an analytical solution, and calculates a probability distribution distance metric.

**Task Details:**
1. **Data Source:** A dataset of 2D coordinates is located at `/home/user/spatial_data.csv`. Each row contains `x,y` coordinates (comma-separated, no header). All points fall within the domain $X \in [0, 1]$ and $Y \in [0, 1]$.
2. **Domain Decomposition & Mesh Refinement:**
   - Start with the domain $[0, 1] \times [0, 1]$.
   - Create an initial $2 \times 2$ grid (4 equal-sized square cells, this is depth 0).
   - **Refinement Rule:** Check the number of points in each cell. If a cell contains **more than 50 points**, recursively split it into 4 equal sub-quadrants. 
   - Continue refinement up to a **maximum depth of 3**. (Depth 0: $2\times2$, Depth 1: a split cell becomes $4$ smaller cells, etc. The maximum possible depth is 3, meaning the smallest possible cell is $1/16 \times 1/16$).
   - A point exactly on a boundary should be assigned to the cell that includes its lower boundary (e.g., $x_{min} \le x < x_{max}$). For the absolute maximum boundaries ($x=1.0$ or $y=1.0$), include them in the uppermost/rightmost cells (i.e., $x \le 1.0$).
3. **Analytical Solution Validation:**
   - The theoretical model is a 2D Gaussian distribution centered at $\mu_x=0.5, \mu_y=0.5$ with standard deviation $\sigma=0.2$.
   - The non-normalized density function is $f(x,y) = \exp\left(-\frac{(x-0.5)^2 + (y-0.5)^2}{2(0.2)^2}\right)$.
   - For each leaf cell $i$ in your final mesh, approximate its theoretical unnormalized mass as $q'_i = f(x_c, y_c) \times \text{Area}_i$, where $(x_c, y_c)$ is the geometric center of cell $i$.
   - Calculate the normalized theoretical probability for each cell: $Q_i = \frac{q'_i}{\sum q'_j}$.
4. **Probability Distribution Distance Metric:**
   - Calculate the empirical probability $P_i$ for each cell: $P_i = \frac{\text{Number of points in cell } i}{\text{Total number of points}}$.
   - Compute the Kullback-Leibler (KL) divergence from $Q$ to $P$: 
     $D_{KL}(P || Q) = \sum_{P_i > 0} P_i \ln\left(\frac{P_i}{Q_i}\right)$
     (Use the natural logarithm. If $P_i = 0$, skip that term as $\lim_{x \to 0} x \ln(x) = 0$).
5. **Output:**
   - The program must write its results to a JSON file at `/home/user/model_fit.json`.
   - The JSON file must have exactly this format:
     ```json
     {
       "total_cells": <integer, total number of leaf cells in the final mesh>,
       "max_depth_reached": <integer, the maximum refinement depth actually reached>,
       "kl_divergence": <float, rounded to 4 decimal places>
     }
     ```

**Requirements:**
- Write your C++ code in `/home/user/spatial_model.cpp`.
- You may install any necessary Ubuntu packages (e.g., `nlohmann-json3-dev`, `build-essential`, `cmake`) using standard `apt` commands.
- Compile and run your program to produce the final `/home/user/model_fit.json` file.