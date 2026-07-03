You are a mobile build engineer maintaining our CI/CD pipelines. We recently performed a schema migration for our device configuration data, moving from a legacy XML format to a simplified V2 Key-Value schema (`/home/user/schema_v2.txt`). 

Since the migration, our CI pipeline is failing because our legacy build scripts cannot process the new constraint expressions that define our dynamic build flags. 

Your task is to write a standalone C program (`/home/user/generate_config.c`) that parses the new schema, evaluates a set of dependency constraints, and generates a valid C header file (`/home/user/build_config.h`).

Here are the details:
1. **Inputs:**
   - `/home/user/schema_v2.txt`: Contains base environment variables in the format `KEY=VALUE` (one per line, where VALUE is a non-negative integer).
   - `/home/user/constraints.txt`: Contains build rules in the format `TARGET = OP1 OPERATOR OP2` (one per line). 
     - `TARGET` is the new build flag to define.
     - `OP1` and `OP2` can be base variables from the schema, integer literals, or other `TARGET` flags defined in this file.
     - `OPERATOR` will be one of: `+`, `*`, `>`, `<`. (For boolean results like `>`, output `1` for true and `0` for false).

2. **Constraint Satisfaction & Expression Parsing:**
   The rules in `constraints.txt` are NOT guaranteed to be in topological order. A rule might reference a `TARGET` that is defined on a later line. Your C program must correctly resolve these dependencies and evaluate the final integer value for all variables. You can assume there are no cyclic dependencies.

3. **Output:**
   Your program must write a generated header to `/home/user/build_config.h`. 
   The file must contain `#define` directives for ALL variables (both the base variables from the schema and the evaluated target flags from the constraints file).
   The `#define` directives must be sorted alphabetically by the variable name.
   Format: `#define <VAR_NAME> <VALUE>\n`

4. **Execution:**
   Compile your tool to `/home/user/generate_config` using standard `gcc`. 
   Run it. It should cleanly produce the `/home/user/build_config.h` file. We will test the correctness of this header file programmatically.