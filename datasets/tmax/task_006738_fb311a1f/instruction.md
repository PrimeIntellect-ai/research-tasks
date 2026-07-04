You are tasked with acting as a configuration manager for a fleet of CNC machines. We store historical configuration files (GCode) in nested archives. You need to analyze the history of extruder calibration settings, apply a bulk update to the latest configurations, and repackage the archives.

**Initial State:**
You have a nested archive at `/home/user/cnc_configs.tar.gz`.
This tarball contains multiple zip files (`node_alpha.zip`, `node_beta.zip`).
Each zip file contains historical configuration files named `v1.gcode`, `v2.gcode`, `v3.gcode`.

**Your Objectives:**

1. **Extract and Track Changes (Domain Parsing):**
   Unpack the nested archives. Write a Python script to parse all `.gcode` files and extract the `E` (Extruder steps/mm) value from the `M92` command.
   *Example GCode line:* `M92 X80.0 Y80.0 Z400.0 E93.5 ; Set axis steps per unit`
   
   Generate a CSV file at `/home/user/extruder_history.csv` with the exact header `Node,Version,E_Value`.
   Sort the CSV alphabetically by Node, then numerically by Version (e.g., v1, v2, v3).
   *Example row:* `node_alpha,v1,93.5`

2. **Bulk Configuration Update (Large-scale text editing):**
   A recent hardware change requires us to update the latest configuration across all nodes. 
   Find all `v3.gcode` files. Parse the `M92` line, extract the current `E` value, add exactly `10.5` to it, and replace the line in the file. Keep the rest of the line (including other axes and comments) exactly intact, just modifying the numeric value after `E`. 
   Format the new E value to 1 decimal place.
   *(Example: `E93.5` becomes `E104.0`)*

3. **Repackage Archives (Nested Archive Handling):**
   Re-zip the modified directories into `node_alpha.zip` and `node_beta.zip`.
   Package these zip files into a new tarball at `/home/user/updated_cnc_configs.tar.gz` matching the original structure exactly (tarball -> zip -> gcode files). Do not include any parent directories in the zip or tar structures.

Write a Python script to perform this workflow or use a combination of Python and bash commands.