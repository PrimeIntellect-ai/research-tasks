You are a data scientist taking over an old data pipeline. 

We have a legacy compiled executable located at `/app/legacy_cleaner` which is used to clean and merge datasets before calculating correlation metrics. Unfortunately, the original C source code was lost, and the binary is stripped. 

We know the binary takes exactly two arguments:
1. `file_x.csv`: A CSV file with a header (e.g., `id,value_x`) containing integer IDs and values.
2. `file_y.csv`: A CSV file with a header (e.g., `id,value_y`) containing integer IDs and values.

From our observations, the binary does the following:
1. Performs an inner join on the `id` column.
2. Performs a data cleaning step by filtering out any joined rows where either `value_x` or `value_y` is strictly less than 0.
3. Computes the product of `value_x` and `value_y` for each valid row (a primitive step for our covariance calculation).
4. Prints the output to `stdout` in the format `id,product`, sorted by `id` in descending numerical order.

Your task is to reverse engineer its exact output format (including how it handles headers and spacing) and write a fully reproducible pipeline script in Bash to replace it. 

Create a Bash script at `/home/user/cleaner.sh` that accepts two CSV file paths as arguments and outputs BIT-EXACT identical results to the `/app/legacy_cleaner` binary for any given inputs. You should run tests against the binary to ensure your output perfectly matches its behavior, including edge cases and headers.

Ensure your script is executable (`chmod +x /home/user/cleaner.sh`).