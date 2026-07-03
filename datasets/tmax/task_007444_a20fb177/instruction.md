You are a data analyst tasked with processing sensor data from two legacy systems. 

You have two input files located in your home directory:
1. `/home/user/sensor_readings.csv` - Contains raw temperature readings at 5 different time steps in a wide format (`Sensor_ID`, `t_0`, `t_1`, `t_2`, `t_3`, `t_4`). Because it was exported from an old Windows CE device, this file is encoded in `UTF-16LE`.
2. `/home/user/sensor_metadata.csv` - Contains calibration data for each sensor (`Sensor_ID`, `Zone`, `Cal_Multiplier`, `Offset`). This file was exported from a European database and is encoded in `ISO-8859-1`.

Your task is to write a Python script that performs the following data processing pipeline:
1. Read both files using their correct character encodings.
2. Reshape the sensor readings from wide format to a long format (so there is one row per sensor per time step).
3. Merge the reshaped readings with the metadata.
4. Calculate the calibrated value for each reading using the mathematical formula: 
   `Calibrated_Value = (Raw_Reading * Cal_Multiplier) + Offset`
5. For each `Sensor_ID`, extract a new mathematical feature: the Euclidean norm (L2 norm) of its 5 `Calibrated_Value`s. 
   *(Recall that the L2 norm of a vector x is the square root of the sum of the squared vector values).*
6. Sort the final aggregated data by the L2 norm in **descending** order. If there is a tie, sort by `Sensor_ID` in ascending alphabetical order.
7. Round the L2 norm to exactly 3 decimal places.
8. Save the final result to `/home/user/calibrated_norms.csv` with exactly two columns: `Sensor_ID` and `L2_Norm`.

Ensure your Python script completely handles this end-to-end pipeline and generates the required output file.