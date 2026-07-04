apt-get update && apt-get install -y python3 python3-pip gcc sqlite3
pip3 install pytest pandas numpy jinja2

mkdir -p /app
cat << 'EOF' > /app/sensor_stream.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

double generate_gaussian_noise(double mu, double sigma) {
    static const double epsilon = 0.0000001;
    static const double two_pi = 2.0*3.14159265358979323846;
    double z1, z0, u1, u2;
    static int generate = 0;
    generate = !generate;
    if (!generate) return z1 * sigma + mu;
    do { u1 = rand() * (1.0 / RAND_MAX); } while (u1 <= epsilon);
    u2 = rand() * (1.0 / RAND_MAX);
    z0 = sqrt(-2.0 * log(u1)) * cos(two_pi * u2);
    z1 = sqrt(-2.0 * log(u1)) * sin(two_pi * u2);
    return z0 * sigma + mu;
}

int main() {
    srand(42);
    printf("timestamp,value\n");
    FILE *truth = fopen("/app/truth_anomalies.json", "w");
    fprintf(truth, "[");
    int first = 1;

    for (int t = 1; t <= 100000; t++) {
        double val = 10.0 * sin(t / 100.0) + 50.0;
        val += generate_gaussian_noise(0, 1.0);

        // Inject anomaly
        if (t > 1000 && rand() % 500 == 0) {
            val += (rand() % 2 == 0 ? 15.0 : -15.0);
            if (!first) fprintf(truth, ",");
            fprintf(truth, "%d", t);
            first = 0;
        }

        printf("%d,%.4f\n", t, val);
    }
    fprintf(truth, "]\n");
    fclose(truth);
    return 0;
}
EOF

gcc -O3 /app/sensor_stream.c -o /app/sensor_stream -lm
strip /app/sensor_stream
chmod +x /app/sensor_stream
/app/sensor_stream > /dev/null
rm /app/sensor_stream.c

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app