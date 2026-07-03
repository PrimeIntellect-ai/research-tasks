apt-get update && apt-get install -y python3 python3-pip g++ make valgrind
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/oracle_processor.cpp
#include <iostream>
#include <string>
#include <iomanip>
#include <deque>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    int K = std::stoi(argv[1]);

    std::deque<double> window;
    double val;
    while (std::cin >> val) {
        if (val == -1.0) {
            window.clear();
            continue;
        }

        if (window.size() == K) {
            window.pop_front();
        }
        window.push_back(val);

        double mean = 0.0;
        double M2 = 0.0;
        int count = 0;

        for (double x : window) {
            count++;
            double delta = x - mean;
            mean += delta / count;
            double delta2 = x - mean;
            M2 += delta * delta2;
        }

        double var = 0.0;
        if (count > 0) {
            var = M2 / count;
        }

        std::cout << std::fixed << std::setprecision(6) << "Mean: " << mean << ", Variance: " << var << std::endl;
    }
    return 0;
}
EOF

    g++ -O3 /app/oracle_processor.cpp -o /app/oracle_processor
    strip /app/oracle_processor
    rm /app/oracle_processor.cpp

    mkdir -p /home/user/workspace
    cat << 'EOF' > /home/user/workspace/processor.cpp
#include <iostream>
#include <string>
#include <iomanip>

struct Node {
    double value;
    Node* next;
    Node(double v) : value(v), next(nullptr) {}
};

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    int K = std::stoi(argv[1]);

    Node* head = nullptr;
    Node* tail = nullptr;
    int size = 0;

    double val;
    while (std::cin >> val) {
        if (val == -1.0) {
            // Reset window
            head = nullptr;
            tail = nullptr;
            size = 0;
            continue;
        }

        Node* newNode = new Node(val);
        if (!head) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
        size++;

        // Compute stats
        double sum = 0, sum_sq = 0;
        Node* curr = head;
        int count = 0;
        while (curr) {
            sum += curr->value;
            sum_sq += curr->value * curr->value;
            curr = curr->next;
            count++;
        }

        double mean = sum / count;
        double var = (sum_sq / count) - (mean * mean);

        std::cout << std::fixed << std::setprecision(6) << "Mean: " << mean << ", Variance: " << var << std::endl;

        if (size > K) {
            Node* temp = head;
            head = head->next;
            size--;
        }
    }
    return 0;
}
EOF

    cat << 'EOF' > /home/user/workspace/Makefile
CXX = g++
CXXFLAGS = -O3 -Wall -Wextra

all: processor

processor: processor.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f processor
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/workspace
    chmod -R 777 /home/user