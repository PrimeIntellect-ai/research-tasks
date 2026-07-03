apt-get update && apt-get install -y python3 python3-pip gawk
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF' > /home/user/compute_stats.sh
#!/bin/bash
awk '{
    sum += $1;
    sumsq += ($1 * $1);
    n++;
    if (n > 1) {
        var = (sumsq / n) - ((sum / n) * (sum / n));
        print sqrt(var);
    } else {
        print 0;
    }
}'
EOF
chmod +x /home/user/compute_stats.sh

python3 -c '
import random
random.seed(42)
with open("/home/user/sensor_data.csv", "w") as f:
    for i in range(500):
        f.write(f"{10.0 + random.random()*0.5:.2f}\n")
    f.write("100000000.1\n")
    f.write("100000000.2\n")
    for i in range(498):
        f.write(f"{10.0 + random.random()*0.5:.2f}\n")
'

chmod -R 777 /home/user