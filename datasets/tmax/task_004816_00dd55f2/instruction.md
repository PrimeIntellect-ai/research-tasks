You are a Data Engineer building a high-performance ETL (Extract, Transform, Load) pipeline for a high-frequency sensor network. To minimize latency and system overhead, the core aggregation logic must be written in C.

I have placed a raw dataset of sensor readings at `/home/user/data_pipeline/raw_sensors.csv`. 
The CSV has no header and contains three columns: `timestamp` (long), `sensor_id` (int), and `value` (double).

Your task is to build a reproducible data pipeline with the following components:

1. **C Aggregation Program (`/home/user/data_pipeline/aggregate.c`)**
   Write a C program that reads `raw_sensors.csv`.
   For each unique `sensor_id`, calculate:
   - Total number of readings (`count`)
   - Minimum value (`min`)
   - Maximum value (`max`)
   - Average value (`avg`)
   
   The program must output a new CSV file to `/home/user/data_pipeline/aggregated.csv` with the header `sensor_id,count,min,max,avg`.
   The rows must be sorted in ascending order by `sensor_id`.
   Format all double values (`min`, `max`, `avg`) to exactly two decimal places (e.g., `%.2f`).

2. **Pipeline Automation (`/home/user/data_pipeline/Makefile`)**
   Create a Makefile to orchestrate the ETL pipeline. It must contain the following targets:
   - `build`: Compiles `aggregate.c` into an executable named `aggregate` using `gcc`. Use `-O3` optimization.
   - `run`: Executes the `aggregate` binary to produce `aggregated.csv`.
   - `test`: A reproducibility test. It should run the `aggregate` binary 3 separate times. After each run, it must compute the `md5sum` of the resulting `aggregated.csv`. Finally, it must output a file `/home/user/data_pipeline/reproducibility_report.txt` exactly in this format:
     ```
     Run 1: <md5sum_hash>
     Run 2: <md5sum_hash>
     Run 3: <md5sum_hash>
     Reproducible: YES
     ```
     (Assuming the hashes match. If they don't, output `Reproducible: NO`).
   - `clean`: Removes the binary, the aggregated CSV, and the report.
   - `all`: Runs `build`, then `run`, then `test`.

Once you have created the `aggregate.c` and `Makefile`, run `make all` to build the pipeline, process the data, and generate the reproducibility report.