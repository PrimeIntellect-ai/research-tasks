You are a data analyst managing a sensor data ingestion pipeline. We receive bulk exports of sensor readings in a "wide" CSV format, but before we bulk-import them into our timeseries database, we need to sanitize, deduplicate, and reshape the data into a "long" format. 

Unfortunately, some recent CSV exports contain corrupted lines or malicious SQL injection payloads in the numeric fields.

Your task is to build a robust C++ data processing tool and a wrapper script:

1. **Extract Configuration**: 
   There is an image at `/app/system_specs.png` that contains the valid sensor column names (which dictate the schema) and a secret `SALT` value used for our deduplication hashes. Extract these values. (You may use Tesseract or other available tools).

2. **Create the C++ Processor**:
   Write a C++ program and compile it to `/home/user/cleaner`. 
   The program must take two arguments: an input CSV path and an output CSV path.
   `Usage: /home/user/cleaner <input_csv> <output_csv>`
   
   The program must perform the following:
   * **Read the wide CSV**: Expected columns are `timestamp` followed by the sensor names extracted from the image.
   * **Sanitize (Adversarial Filtering)**: Validate every row. If *any* sensor value in a row contains characters other than valid numeric characters (digits `0-9`, at most one decimal point `.`, and an optional leading minus sign `-`), the entire row is considered "evil" and must be dropped completely.
   * **Reshape**: Convert the valid wide rows into long format. For a wide row with 3 sensors, output 3 long rows.
   * **Deduplication Hash**: The long format output must be `timestamp,sensor_name,value,hash`. 
     The `hash` must be a 64-bit unsigned integer generated using `std::hash<std::string>` on the exact string `<timestamp>_<sensor_name>_<value>_<SALT>`, where `<SALT>` is the exact string extracted from the image.

3. **Parallel Processing Script**:
   Write a bash script at `/home/user/process_all.sh` that takes an input directory and an output directory as arguments. It must find all `.csv` files in the input directory and process them using your C++ `/home/user/cleaner` program in parallel (e.g., using `xargs -P` or background jobs).

The system will verify your `/home/user/cleaner` binary against a hidden adversarial corpus consisting of "clean" and "evil" CSV files to ensure 100% of malicious rows are rejected and 100% of clean rows are correctly transformed.