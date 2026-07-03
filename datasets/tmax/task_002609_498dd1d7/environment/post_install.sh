apt-get update && apt-get install -y python3 python3-pip festival g++
pip3 install pytest

mkdir -p /app

echo "Hello. For the upcoming polynomial regression tests over the finite field, please use the prime modulus eight thousand one hundred ninety one. Ensure your C++ program outputs the coefficients exactly in the format: C zero equals, C one equals, C two equals, separated by commas. Thank you." | text2wave -o /app/dictation.wav || true

cat << 'EOF' > /tmp/oracle_polyfit.cpp
#include <iostream>
#include <vector>
#include <string>

long long modInverse(long long n, long long p) {
    long long t = 0, newt = 1;
    long long r = p, newr = n;
    while (newr != 0) {
        long long quotient = r / newr;
        long long temp = t - quotient * newt;
        t = newt; newt = temp;
        temp = r - quotient * newr;
        r = newr; newr = temp;
    }
    if (r > 1) return -1;
    if (t < 0) t = t + p;
    return t;
}

int main(int argc, char* argv[]) {
    if (argc != 7) return 1;
    long long p = 8191;
    long long x1 = std::stoll(argv[1]) % p;
    long long y1 = std::stoll(argv[2]) % p;
    long long x2 = std::stoll(argv[3]) % p;
    long long y2 = std::stoll(argv[4]) % p;
    long long x3 = std::stoll(argv[5]) % p;
    long long y3 = std::stoll(argv[6]) % p;

    auto eval_denom = [&](long long xa, long long xb, long long xc) {
        long long d1 = (xa - xb + p) % p;
        long long d2 = (xa - xc + p) % p;
        return (d1 * d2) % p;
    };

    long long d1 = eval_denom(x1, x2, x3);
    long long d2 = eval_denom(x2, x1, x3);
    long long d3 = eval_denom(x3, x1, x2);

    long long inv1 = modInverse(d1, p);
    long long inv2 = modInverse(d2, p);
    long long inv3 = modInverse(d3, p);

    long long c0 = 0, c1 = 0, c2 = 0;

    auto add_term = [&](long long yi, long long inv, long long a, long long b) {
        long long weight = (yi * inv) % p;
        long long term0 = (a * b) % p;
        long long term1 = (p - ((a + b) % p)) % p;
        long long term2 = 1;

        c0 = (c0 + weight * term0) % p;
        c1 = (c1 + weight * term1) % p;
        c2 = (c2 + weight * term2) % p;
    };

    add_term(y1, inv1, x2, x3);
    add_term(y2, inv2, x1, x3);
    add_term(y3, inv3, x1, x2);

    std::cout << "C0=" << c0 << ", C1=" << c1 << ", C2=" << c2 << "\n";
    return 0;
}
EOF

g++ -O3 /tmp/oracle_polyfit.cpp -o /app/oracle_polyfit

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user