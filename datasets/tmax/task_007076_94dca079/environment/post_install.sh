apt-get update && apt-get install -y python3 python3-pip gcc make ruby
    pip3 install pytest

    mkdir -p /home/user/polyglot_math
    cd /home/user/polyglot_math

    cat << 'EOF' > generate_primes.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    if(argc != 2) return 1;
    int n = atoi(argv[1]);
    if(n < 2) return 0;
    int *sieve = calloc(n+1, sizeof(int));
    for(int p=2; p<=sqrt(n); p++) {
        if(sieve[p] == 0) {
            for(int i=p*p; i<=n; i+=p) sieve[i] = 1;
        }
    }
    for(int p=2; p<=n; p++) {
        if(sieve[p] == 0) printf("%d\n", p);
    }
    free(sieve);
    return 0;
}
EOF

    cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-Wall -O2

all: generate_primes

generate_primes: generate_primes.c
    $(CC) $(CFLAGS) -o generate_primes generate_primes.c

clean:
    rm -f generate_primes
EOF

    cat << 'EOF' > collatz.rb
ARGF.each_line do |line|
  n = line.to_i
  next if n <= 0
  orig = n
  steps = 0
  while n != 1
    if n % 2 == 0
      n = n / 2
    else
      n = 3 * n + 1
    end
    steps += 1
  end
  puts "#{orig},#{steps}"
end
EOF

    cat << 'EOF' > expected_output.txt
2,1
5,5
3,7
13,9
53,11
17,12
11,14
23,15
7,16
29,18
61,19
19,20
37,21
67,27
43,29
89,30
59,32
79,35
71,102
47,104
31,106
41,109
83,110
73,115
97,118
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/polyglot_math
    chmod -R 777 /home/user