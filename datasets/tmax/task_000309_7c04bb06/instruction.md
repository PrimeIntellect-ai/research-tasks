You are an AI assistant helping a data science researcher organize and analyze a text dataset, then serve the results and visualizations via a secure API.

We have a dataset located at `/home/user/data/texts.csv` with two columns: `group` (either 'Control' or 'Treatment') and `text` (a sentence or paragraph).

Your task has three phases:

**Phase 1: Data Processing & Statistical Analysis**
1. Read `/home/user/data/texts.csv`.
2. Tokenize the `text` column into individual words:
   - Convert all text to lowercase.
   - Remove the following punctuation characters entirely: `.`, `,`, `!`, `?`
   - Split the text into tokens by whitespace.
3. For each document, calculate the mean token length (average number of characters per token).
4. Perform a two-sided Welch's t-test (assuming unequal variances) to compare the document mean token lengths between the 'Control' group and the 'Treatment' group.
5. Calculate the 95% confidence interval for the difference in means (Treatment mean - Control mean). 

**Phase 2: Fixing the Vendored Visualization Package**
We use a custom, proprietary package for our lab's plots, located at `/app/research-viz-pkg`. 
Currently, the package is misconfigured for headless server environments: it runs without error, but it produces completely blank (or virtually empty) image files due to a backend misconfiguration in its source code.
1. Inspect the source code of the package in `/app/research-viz-pkg`.
2. Fix the misconfiguration so it generates valid plots without requiring a display server.
3. Install the fixed package in your environment.
4. Use the package's `generate_boxplot(control_data, treatment_data, output_path)` function to generate a boxplot of the mean token lengths for the two groups, saving it to `/home/user/plot.png`.

**Phase 3: Serving the Results**
Create a Python HTTP web service that serves your findings. 
1. The service must listen on `0.0.0.0` port `8080`.
2. It must require a specific HTTP header for authentication: `X-Research-Token: sigma-99-alpha`.
3. It must implement the following routes:
   - `GET /stats`: Returns a JSON response exactly matching this structure:
     `{"t_stat": <float>, "p_value": <float>, "ci_lower": <float>, "ci_upper": <float>}`
     *(Round all floats to 4 decimal places. The CI is Treatment minus Control).*
   - `GET /plot`: Returns the `plot.png` generated in Phase 2 with the correct image MIME type.

Start your server as a background process or leave it running in your final command so that our automated systems can query it.