You are a data scientist working on a dataset that needs to be cleaned and fed into a simple C++ linear regression model. 

You have been provided with two files in your home directory (`/home/user/`):
1. `raw_data.csv` - A dataset with two columns: `X` and `Y`. This dataset is corrupted. It contains a header, some rows where `X` is 'NaN', and some rows where `X` is negative.
2. `train.cpp` - A C++ program that reads a headerless, comma-separated CSV file (passed as the first command-line argument), computes a simple Ordinary Least Squares (OLS) linear regression model ($Y = \text{Slope} \cdot X + \text{Intercept}$), and prints the parameters.

Your task is to:
1. Use standard Linux shell utilities to clean `raw_data.csv`. You must remove the header row, remove any row containing the string 'NaN', and remove any row where the value of `X` is strictly less than 0. Save the cleaned data to `/home/user/cleaned_data.csv`.
2. Compile the `train.cpp` file using `g++` into an executable named `train_model` in the `/home/user/` directory.
3. Run the compiled `train_model` executable on your `cleaned_data.csv` file.
4. Redirect the standard output of the model training executable to exactly `/home/user/model_output.txt`.

Ensure your final output file `model_output.txt` contains only the exact output produced by the C++ program running on the correctly cleaned dataset.