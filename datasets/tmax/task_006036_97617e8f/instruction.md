You are a Data Engineer tasked with building a reproducible ETL pipeline in Go that enforces a data schema, applies dimensionality reduction using a numerical library, and stores the processed data in a local database.

You must build this pipeline in `/home/user/pipeline/`.

**1. Data Ingestion & Schema Enforcement**
You are provided with a raw JSONL file at `/home/user/data/raw_metrics.jsonl`.
Each line is a JSON object. You must enforce the following schema:
- Must have a `record_id` (string) which is not empty.
- Must have `features` (array of numbers).
- The `features` array must contain exactly 8 elements.
Any record failing these rules must be silently dropped. 

**2. Dimensionality Reduction**
For each valid record, you must reduce the 8-dimensional feature vector to 3 dimensions using Gaussian Random Projection.
- Use `gonum.org/v1/gonum/mat` for matrix operations.
- Initialize a dense projection matrix $R$ of size $8 \times 3$.
- Populate $R$ using `math/rand`. You MUST create a local random source seeded with `99` (i.e., `rand.New(rand.NewSource(99))`). 
- Fill the matrix $R$ row-by-row, column-by-column (i.e., $R_{0,0}, R_{0,1}, R_{0,2}, R_{1,0} \dots R_{7,2}$) using your local random generator's `NormFloat64()` method.
- For each valid record, represent its features as a $1 \times 8$ dense matrix $F$.
- Compute the reduced feature matrix $X = F \times R$. $X$ will be a $1 \times 3$ matrix containing the new projected features $p_1, p_2, p_3$.

**3. Data Storage Management**
Save the reduced records into a SQLite3 database at `/home/user/pipeline/results.db`.
- Use `github.com/mattn/go-sqlite3`.
- Create a table named `projections` with the following schema:
  - `record_id` (TEXT PRIMARY KEY)
  - `p1` (REAL)
  - `p2` (REAL)
  - `p3` (REAL)
- Insert the valid, reduced records into this table.

**4. Reproducible Pipeline**
Write a self-contained bash script at `/home/user/pipeline/build_and_run.sh` that:
1. Initializes a Go module (if not already done).
2. Installs required dependencies (`gonum` and `go-sqlite3`).
3. Builds the Go program.
4. Executes the Go program to read the data, process it, and create `results.db`.

Make sure your script correctly configures the environment for `go-sqlite3` (which requires CGO). Ensure the final state of the system contains the populated `results.db`.