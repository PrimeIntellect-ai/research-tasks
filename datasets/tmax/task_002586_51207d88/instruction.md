You are a bioinformatics analyst processing a recent batch of qPCR data and extracting cloning information from a sequence.

Your tasks are as follows:

1. **Overhang Extraction**: 
You have a DNA sequence located in `/home/user/sequence.txt`. Find the first occurrence of the BsaI restriction site (`GGTCTC`). Extract the 4 nucleotides immediately following this site, compute their reverse complement (A<->T, C<->G, and reverse the string), and save the 4-bp reverse-complemented string to `/home/user/overhang.txt`.

2. **qPCR Data Analysis**:
You have a CSV file `/home/user/qpcr_data.csv` containing simulated qPCR fluorescence data for a 96-well plate. The file has 96 rows (representing the wells) and 40 columns (representing cycles 1 through 40).
- For each well (row), isolate the fluorescence data for cycles 5 through 15 (inclusive). Note that column 1 corresponds to cycle 1.
- Fit an exponential growth curve of the form `y = A * exp(r * x)` to this isolated data, where `x` is the cycle number (from 5 to 15) and `y` is the fluorescence. You can use `scipy.optimize.curve_fit` with an initial guess of `A=10` and `r=0.2`.
- Extract the growth rate `r` for each of the 96 wells.
- Reshape the 96 `r` values into an 8x12 multi-dimensional array (representing the 8 rows and 12 columns of the plate, in row-major order).
- Calculate the maximum growth rate `r` for each of the 12 columns.
- Save these 12 maximum values as a comma-separated string, with each value rounded to exactly 4 decimal places, to `/home/user/col_max_r.txt`.

You must write and execute Python scripts to perform these operations.