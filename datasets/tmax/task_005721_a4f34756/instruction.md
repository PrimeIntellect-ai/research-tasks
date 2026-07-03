I am trying to fit a simple linear model ($y = wx$) to a dataset of observations, but my bash script keeps diverging and outputting `nan` or `inf`. 

The data is stored as a 2D array (N rows, 2 columns for X and Y) in an HDF5 file located at `/home/user/dataset.h5` under the dataset name `/observations`. 

I have a script at `/home/user/fit.sh` that uses `h5dump` and `awk` to parse the multi-dimensional HDF5 data and perform gradient descent. However:
1. It looks like the system is missing the necessary command-line tools to read HDF5 files.
2. The gradient descent diverges because the step-size adaptation (learning rate) is set way too high for this data scale.

Your task is to:
1. Install the required tools to process HDF5 files in the terminal.
2. Fix the `/home/user/fit.sh` script so that it properly converges. You should lower the learning rate (`lr`) in the awk script to a sensible value (e.g., `0.01`) so that the weights stabilize. 
3. Run the fixed script and save the final output weight (which the script prints) into a file named `/home/user/weight.txt`.

Ensure the final weight in `/home/user/weight.txt` is correct and does not diverge.