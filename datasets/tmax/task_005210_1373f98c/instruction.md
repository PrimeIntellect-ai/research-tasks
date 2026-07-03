You are a data engineer building an ETL pipeline to process time-series temperature data from legacy industrial sensors.

We have raw data from two sensors in `/home/user/data/`:
1. `sensor_a.csv` 
   - Encoding: UTF-16LE
   - Format: `timestamp,temp_c` (e.g., `2023-10-01 04:00:00,12.5`)
   - Temperature unit: Celsius
2. `sensor_b.csv`
   - Encoding: ISO-8859-1
   - Format: `timestamp,temp_f` (e.g., `10/01/2023-08:00,59.0` - Note the MM/DD/YYYY-HH:MM format)
   - Temperature unit: Fahrenheit

Your task is to write a Python script at `/home/user/etl.py` that performs the following steps when executed:
1. **Extract and Handle Encoding**: Read both files using their correct character encodings.
2. **Normalize**: 
   - Parse the timestamps and normalize them to a daily date representation (`YYYY-MM-DD`).
   - Convert all temperatures to Celsius (Formula: `C = (F - 32) * 5.0 / 9.0`).
3. **Aggregate**: Combine data from both sensors and calculate the daily minimum, maximum, and average temperatures (in Celsius). Round the average to exactly 2 decimal places.
4. **Generate Report**: Use the template located at `/home/user/template.md` to generate a single markdown file at `/home/user/output/report.md`. 
   - The output file must contain the template repeated and populated for each unique date, sorted chronologically ascending.
   - Separate each daily block with a blank line.

Here is the exact text of `/home/user/template.md` (do not alter its structure, just replace the placeholders):
```markdown
## Report for {DATE}
Min: {MIN} C
Max: {MAX} C
Avg: {AVG} C
```

Run your script so that `/home/user/output/report.md` is generated.