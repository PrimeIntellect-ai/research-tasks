You are a data analyst who needs to process a CSV dataset into a specific projected vector format using Rust. 

There is a dataset located at `/home/user/data.csv` with two columns: `id` (integer) and `text` (string).
Your task is to write and execute a Rust program that performs the following steps:

1. **Tokenization & Frequency Extraction**: 
   Read the CSV file. For each row's `text`, convert the string to lowercase and split it into tokens using any non-alphabetic character as the delimiter (i.e., tokens should consist strictly of the English letters a-z). 
   Count the occurrences of the following 5 specific vocabulary words in the text:
   - Index 0: `data`
   - Index 1: `science`
   - Index 2: `rust`
   - Index 3: `matrix`
   - Index 4: `vector`
   
   This step yields a 1x5 row vector of integers for each CSV row (representing the counts of these 5 words).

2. **Linear Algebra Transformation**:
   Multiply the 1x5 frequency vector by a fixed 5x2 transformation matrix to project the data into a 2D space. 
   The projection matrix `M` (where `Result = FrequencyVector * M`) is defined as:
   Row 0 (for `data`):    `[1.0, 0.5]`
   Row 1 (for `science`): `[0.0, 1.0]`
   Row 2 (for `rust`):    `[-1.0, 0.0]`
   Row 3 (for `matrix`):  `[0.5, -0.5]`
   Row 4 (for `vector`):  `[0.0, 0.2]`

3. **Data Schema Enforcement (Binary Output)**:
   Write the projected 2D results for each row to a strictly formatted binary file located at `/home/user/output.bin`.
   For each row in the CSV (in the same order), write exactly 12 bytes using Little Endian byte order:
   - `id`: unsigned 32-bit integer (4 bytes)
   - `val1`: 32-bit float (4 bytes) - the first component of the projected 2D vector
   - `val2`: 32-bit float (4 bytes) - the second component of the projected 2D vector

Your solution should create a Rust project in `/home/user/proj`, build it, run it, and successfully generate the `/home/user/output.bin` file. You may use standard Rust crates (like `csv`, `byteorder`) by adding them to your `Cargo.toml`.