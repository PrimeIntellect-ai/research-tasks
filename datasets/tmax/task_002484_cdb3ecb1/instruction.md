You are a data scientist analyzing a biological sequence similarity network. You've exported the network's adjacency graph into a FITS file located at `/home/user/data/matrix.fits` (the primary HDU contains a 2D float64 image/matrix). 

Currently, your model fitting pipeline is failing. It attempts to solve a linear system based on this similarity matrix, but the matrix is near-singular due to highly identical biological sequences (duplicate information), causing the matrix factorization to fail or produce wildly unstable outputs.

Your task is to write a Go program at `/home/user/solve.go` to safely solve the system by applying Tikhonov regularization (Ridge regression).

The program must perform the following:
1. Read the 2D float64 matrix from the primary HDU of `/home/user/data/matrix.fits`. (You may use `github.com/astrogo/fitsio`).
2. Construct a dense matrix $A$ using `gonum.org/v1/gonum/mat`.
3. Apply Tikhonov regularization by adding $\lambda I$ to the matrix, where $I$ is the identity matrix and the regularization parameter $\lambda = 0.05$. Let this new matrix be $A'$.
4. Solve the linear system $A' x = b$, where $b$ is a vector of exactly $1.0$s with a length equal to the number of rows in $A$.
5. Write the resulting solution vector $x$ as a flat JSON array of floating-point numbers to `/home/user/solution.json`.

Please initialize a Go module in `/home/user`, install the required dependencies, write the code, and execute it to generate the `solution.json` file.