As a machine learning engineer, I need to generate a spatial dataset to train a binary classifier that predicts whether a point lies inside a unit circle ($x^2 + y^2 \le 1$). 

To ensure the boundary features are captured with sufficient resolution, you must write a Rust program that generates this data using a parallelized grid-based approach with iterative mesh refinement and a convergence test.

Please create a Rust project named `circle_data_gen` in `/home/user/`. Use `rayon` for parallelizing the grid evaluations.

Your Rust program must do the following:
1. Define a 2D square domain from $[-1, 1] \times [-1, 1]$.
2. Start with a grid resolution of $N = 10$ (which means $N \times N$ cells).
3. The width and height of each cell is $d = 2.0 / N$. 
4. The center of the $(i, j)$-th cell is $x_i = -1.0 + (i + 0.5) \times d$, and $y_j = -1.0 + (j + 0.5) \times d$, for $i, j \in [0, N-1]$.
5. Using `rayon`, evaluate all cell centers in parallel to check if they fall inside the unit circle ($x^2 + y^2 \le 1.0$).
6. Calculate the approximate area of the circle as `Area = (number of cells inside) * d^2`.
7. Append a line to `/home/user/convergence.log` formatted exactly as: `N={N}, Area={Area:.5f}` (e.g., `N=10, Area=3.12000`).
8. **Convergence Test**: If the absolute difference between the current `Area` and the `Area` from the *previous* grid resolution (previous $N$) is less than or equal to `1e-3`, stop the refinement loop. (For the first iteration $N=10$, there is no previous area, so always proceed to the next step).
9. If not converged, double the resolution ($N = 2 \times N$) and repeat steps 3-8.
10. Once convergence is reached, save the evaluated grid centers for the *final, converged $N$* to a CSV file at `/home/user/training_data.csv`. The CSV must have the header `x,y,label`. The `label` is `1` if the point is inside the unit circle, and `0` otherwise. The order of rows in the CSV does not matter.

Ensure you compile and run your Rust program so the `.log` and `.csv` files are generated successfully.