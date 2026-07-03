apt-get update && apt-get install -y python3 python3-pip gcc make gawk bc
pip3 install pytest

# Create directories
mkdir -p /app/stats-tools
mkdir -p /opt/oracle

# Write the vendored package source
cat << 'EOF' > /app/stats-tools/mcmc_estimate.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if (argc != 5) return 1;
    double o1 = atof(argv[1]);
    double o2 = atof(argv[2]);
    double e1 = atof(argv[3]);
    double e2 = atof(argv[4]);

    // Dummy MCMC posterior mean approximation calculation
    double posterior = sqrt(fabs(o1 - e1)) + log(fabs(o2 - e2) + 1.0);
    printf("%.3f\n", posterior);
    return 0;
}
EOF

# Write the broken Makefile
cat << 'EOF' > /app/stats-tools/Makefile
all: mcmc_estimate

mcmc_estimate: mcmc_estimate.c
	gcc -O2 -o mcmc_estimate mcmc_estimate.c
EOF

# Write the Oracle script
cat << 'EOF' > /opt/oracle/analyze_oracle.sh
#!/bin/bash
O1=$1
O2=$2
E1=$3
E2=$4

if [ "$E1" -eq 0 ] || [ "$E2" -eq 0 ]; then
    echo "ERROR: Zero expectation"
    exit 0
fi

chi2=$(awk -v o1="$O1" -v o2="$O2" -v e1="$E1" -v e2="$E2" 'BEGIN {
    chi = ((o1 - e1)^2)/e1 + ((o2 - e2)^2)/e2
    printf "%.6f", chi
}')

# Format to 2 decimal places for the acceptance test
chi2_formatted=$(awk -v c="$chi2" 'BEGIN { printf "%.2f", c }')

is_reject=$(awk -v c="$chi2" 'BEGIN { if (c >= 4.00) print 1; else print 0 }')

if [ "$is_reject" -eq 1 ]; then
    # Must use the compiled binary, assuming it was fixed in the setup for the oracle
    mcmc_out=$(/app/stats-tools/mcmc_estimate "$O1" "$O2" "$E1" "$E2")
    echo "REJECT: $mcmc_out"
else
    echo "ACCEPT: $chi2_formatted"
fi
EOF

chmod +x /opt/oracle/analyze_oracle.sh

# Pre-compile for the oracle
gcc -O2 -o /app/stats-tools/mcmc_estimate /app/stats-tools/mcmc_estimate.c -lm

# Grant wide permissions
chmod -R 777 /app/stats-tools

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user