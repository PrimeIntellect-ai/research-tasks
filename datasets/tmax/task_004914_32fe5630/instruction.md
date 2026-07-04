You are an AI assistant helping a climate researcher organize and analyze a messy, fragmented dataset of environmental sensor readings. 

The dataset is located at `/home/user/sensor_data/`. It contains multiple subdirectories representing different sensor deployment sites (e.g., `site_alpha`, `site_beta`).
Inside these directories are files containing daily readings. However, the data format is inconsistent:
1. Some files are in CSV format (`.csv`), with the header `timestamp,temperature,humidity`.
2. Some files are in JSON Lines format (`.jsonl`), where each line is a JSON object like `{"ts": 1682930000, "t": 24.5, "h": 41.2}`.

Your task consists of three phases:

**Phase 1: Data Normalization (Text Transformation)**
Using shell utilities (like `sed`, `awk`, or `grep`), find all `.jsonl` files in the `/home/user/sensor_data/` directory tree and convert them into `.csv` files in the same directories. 
- The new CSV files should have the exact same name as the original but with a `.csv` extension.
- The new CSV files MUST have the header `timestamp,temperature,humidity`.
- Extract the values for `ts` (timestamp), `t` (temperature), and `h` (humidity) and format them as comma-separated values.
- Once successfully converted, you may leave or delete the original `.jsonl` files.

**Phase 2: Data Aggregation Engine (C Programming)**
Write a C program at `/home/user/aggregate.c`. This program must:
1. Recursively traverse the `/home/user/sensor_data/` directory to find all `.csv` files.
2. Parse each CSV file. 
3. Calculate the global maximum temperature, minimum temperature, and the overall average temperature across *all* valid records from all CSV files.
4. **Data Validation:** Ignore any record where the humidity is less than 0.0 or greater than 100.0, or where the temperature is less than -50.0 or greater than 60.0.

**Phase 3: Generating Structured Output**
Your C program should output the final calculated metrics to a file located at `/home/user/final_results.xml`. The output must strictly follow this exact XML format (format floats to exactly two decimal places):

```xml
<results>
    <metrics>
        <max_temp>XX.XX</max_temp>
        <min_temp>XX.XX</min_temp>
        <avg_temp>XX.XX</avg_temp>
    </metrics>
</results>
```

**Execution:**
- Compile your C program using `gcc -O3 -o /home/user/aggregate /home/user/aggregate.c`.
- Run your executable to generate the final XML file.
- Verify the contents of `/home/user/final_results.xml` before finishing.