apt-get update && apt-get install -y python3 python3-pip gawk
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    # Generate the dataset using Python
    cat << 'EOF' > generate_data.py
import random
import math

random.seed(42)
with open('/home/user/sensor_data.csv', 'w') as f:
    f.write("id,sensor_reading\n")
    # Generate 1000 valid normal points (mean=50, std=10)
    valid_points = []
    for i in range(1, 1001):
        val = random.gauss(50, 10)
        valid_points.append((i, val))

    # Generate 20 extreme outliers (z > 2.0 or z < -2.0 guaranteed)
    for i in range(1001, 1011):
        valid_points.append((i, random.uniform(100, 150)))
    for i in range(1011, 1021):
        valid_points.append((i, random.uniform(-50, 0)))

    # Generate 30 invalid points
    invalids = ["NaN", "missing", "N/A", "12.3.4", "abc", ""] * 5
    for i in range(1021, 1051):
        valid_points.append((i, invalids[i-1021]))

    # Shuffle
    random.shuffle(valid_points)

    for i, (idx, val) in enumerate(valid_points):
        if isinstance(val, float):
            f.write(f"{idx},{val:.4f}\n")
        else:
            f.write(f"{idx},{val}\n")
EOF
    python3 generate_data.py
    rm generate_data.py

    # Pre-calculate the expected clean_output.csv to verify against
    cat << 'EOF' > /tmp/expected_pipeline.sh
#!/bin/bash
export LC_NUMERIC=C
awk -F',' '
NR>1 {
    if ($2 ~ /^-?[0-9]+(\.[0-9]+)?$/) {
        sum += $2
        sumsq += $2*$2
        count++
    }
}
END {
    mean = sum / count
    variance = (sumsq / count) - (mean * mean)
    stddev = sqrt(variance)
    print "id,sensor_reading" > "/home/user/expected_clean.csv"
    while((getline < "/home/user/sensor_data.csv") > 0) {
        if(FNR>1 && $2 ~ /^-?[0-9]+(\.[0-9]+)?$/) {
            z = ($2 - mean) / stddev
            abs_z = z < 0 ? -z : z
            if (abs_z <= 2.0) {
                print $0 >> "/home/user/expected_clean.csv"
            }
        }
    }
}' /home/user/sensor_data.csv
EOF
    bash /tmp/expected_pipeline.sh
    rm /tmp/expected_pipeline.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user