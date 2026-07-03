We are upgrading our configuration management system and need to process a large batch of legacy configuration files to a normalized JSON format, before compressing them with our proprietary archive tool. 

You have been provided a directory of legacy `.conf` files at `/home/user/configs/`. Each file contains key-value pairs in the format `key = value`, along with blank lines and comments (lines starting with `#` or inline comments where `#` appears after a value). 

Your task is to write a **C++ program** (`/home/user/normalize.cpp`) that performs the following steps for every `.conf` file:
1. **Text Transformation & Interpretation:** Parse the configuration, stripping all comments (both full-line and inline) and ignoring blank lines. Trim any leading/trailing whitespace from both keys and values.
2. **Format Conversion:** Convert the parsed data into a flat JSON object (all values should be strings). To maximize dictionary-based compression later, **sort the JSON keys alphabetically**. 
3. **Atomic Writes:** Write the resulting JSON to `/home/user/processed/<filename>.json`. You *must* use atomic writes: write the JSON data to a temporary file first (e.g., `<filename>.json.tmp`), then atomically rename it to the final `.json` file to simulate safe config updates.
4. **Compression:** Once a JSON file is atomically written, invoke our proprietary stripped binary `/app/json_compressor` on it. The syntax is `/app/json_compressor <input.json> <output.jc>`. Put the output `.jc` files in `/home/user/processed/`.

**Evaluation:**
The automated test will evaluate the effectiveness of your normalization by calculating the global compression ratio across the dataset. 
*Metric:* `Total Size of Original .conf Files / Total Size of .jc Files`
Because the proprietary compressor relies heavily on structural predictability, successfully removing noise (comments/spaces) and standardizing the schema (sorting keys) will drastically improve the compression ratio. You must achieve a **compression ratio >= 2.8**.

Compile your C++ program and execute the full pipeline so that `/home/user/processed/` is populated with the final `.json` and `.jc` files.