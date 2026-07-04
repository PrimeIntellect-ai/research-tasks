You are a research assistant organizing a new batch of experimental datasets. We have incoming data files in `/home/user/data/` that need to be validated, processed mathematically, and logged. 

Please perform the following tasks:

1. **Numerical Library Configuration:**
   Install the GNU Scientific Library (GSL) development package (`libgsl-dev`) on this system.

2. **Data Schema Enforcement & Processing Program:**
   Write a C program at `/home/user/process_data.c` and compile it to `/home/user/process_data`. The program must take a single file path as a command-line argument.
   
   For the given CSV file, your C program must enforce the following schema:
   - Every line must contain exactly two comma-separated fields.
   - Both fields must be valid floating-point numbers.
   
   If the file violates this schema in any way (e.g., wrong number of columns, non-numeric strings, empty lines that aren't purely EOF), the program should print EXACTLY the string `SCHEMA_ERROR` to standard output.
   
   If the file is completely valid, the program must extract all the values from the **second column** into an array and use the GSL library function `gsl_stats_variance` to compute the sample variance of that column. The program should then print the variance to standard output, formatted to exactly 4 decimal places (e.g., `6.3333`).

3. **Experiment Tracking:**
   Create a bash script at `/home/user/run_experiments.sh` that:
   - Iterates through all `.csv` files in `/home/user/data/` in alphabetical order.
   - Runs `/home/user/process_data` on each file.
   - Logs the results into an experiment tracking file at `/home/user/tracker.csv`.
   
   The format for `/home/user/tracker.csv` must be:
   `<absolute_file_path>,<output_from_C_program>`
   
   For example, a line in the tracker file might look like:
   `/home/user/data/exp1.csv,6.3333`
   or
   `/home/user/data/exp3.csv,SCHEMA_ERROR`

Run your bash script so that `/home/user/tracker.csv` is generated and fully populated.