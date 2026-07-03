Wake up! It's 3:00 AM and you've just been paged. Our mission-critical sensor processing pipeline is completely down after a botched system migration. 

There are three cascading issues you need to fix immediately to get production back online:

1. **Package Installation Failure**: The deployment failed to install our internal C-optimized distance library. The source is located at `/app/vendored/py-fast-distance`. When you try to install it (`pip install -e /app/vendored/py-fast-distance`), it fails with a linker error. You need to interpret the compiler/linker error, patch the package's configuration, and install it into the system Python environment.
2. **Query Result Anomaly**: The main processing script is located at `/home/user/pipeline.py`. It connects to an SQLite database provided as a command-line argument. The SQL query in the script is currently returning incorrect rows. It is supposed to retrieve data *only* for sensors where `status = 'ACTIVE'`, and it must perform an `INNER JOIN` with the `calibration` table on `sensor_id` to get the `factor` column. 
3. **Formula Logic Error**: The `pipeline.py` script applies a scoring formula. The previous engineer made a typo in the math formula. The code currently calculates `score = fast_distance.compute(lat, lon) + factor`. The correct formula dictated by our physics team is `score = fast_distance.compute(lat, lon) * factor`.

**Your Objective:**
1. Fix the linker error and successfully install the vendored package.
2. Fix the SQL query and the math formula in `/home/user/pipeline.py`.

The script `/home/user/pipeline.py` must take exactly one argument (the path to an SQLite database) and print the computed scores to standard output, one floating-point number per line (rounded to 4 decimal places), sorted by `sensor_id` ascending. 

An automated fuzzer will run your fixed `/home/user/pipeline.py` against dynamically generated databases and compare your standard output bit-for-bit against our proprietary oracle implementation.