You are an AI assistant helping a climate researcher organize and extract insights from a messy, undocumented dataset of field observations.

You have been provided with a large dataset at `/home/user/observations.jsonl`. This file contains roughly 50,000 JSON lines. The data model is undocumented, highly nested, and contains polymorphic fields (a mix of old and new sensor data formats). 

Your objective is to reverse engineer the implicit schema, build an efficient aggregation pipeline, and output strictly validated data.

**Requirements:**

1. **Data Model Reverse Engineering:** 
   Analyze `/home/user/observations.jsonl`. You need to identify how to extract three pieces of information for records where the sensor is marked as "active" or "calibrated" (the status flag might be buried under different keys depending on the sensor version):
   - The region / biome name.
   - The temperature reading (ensure you are extracting Celsius; some older sensors might use a different scale or key, but for this task, only include records where a valid Celsius temperature can be identified).
   - The sensor ID.

2. **Aggregation Pipeline:**
   Write a Python script at `/home/user/process_observations.py` that processes this data.
   - Filter for active/calibrated sensors.
   - Group the data by the region/biome.
   - Calculate the average temperature per region.
   - Count the total number of unique active sensors in that region.

3. **Output Schema Validation:**
   Your script must use `pydantic` to validate the aggregated results before saving. The final output must strictly conform to this schema:
   ```python
   class RegionStats(BaseModel):
       region_name: str
       average_temperature: float
       unique_sensor_count: int

   class FinalOutput(BaseModel):
       results: List[RegionStats]
   ```

4. **Performance & Optimization:**
   The dataset is somewhat large. Your Python script must complete the aggregation and validation in under 5 seconds. Avoid loading the entire dataset into memory at once if possible; optimize your data structures and parsing strategy.

5. **Output:**
   The validated final result must be serialized to JSON and saved to `/home/user/validated_regions.json`. The JSON should perfectly match the `FinalOutput` pydantic model structure.

**Constraints:**
- Use only Python 3 and standard libraries, plus `pydantic`. You may install `pydantic` via pip.
- Do not modify the original `/home/user/observations.jsonl` file.

Write the script and run it to produce the final `validated_regions.json` file.