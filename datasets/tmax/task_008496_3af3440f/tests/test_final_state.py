# test_final_state.py
import os
import subprocess
import pytest

def get_expected_ci():
    cpp_code = """
#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <random>
#include <algorithm>
#include <iomanip>

using namespace std;

int main() {
    ifstream in("/home/user/network_data.txt");
    if (!in) {
        cerr << "Could not open /home/user/network_data.txt" << endl;
        return 1;
    }
    int N;
    in >> N;
    vector<int> distances;
    for (int i = 0; i < N; ++i) {
        int V, E;
        in >> V >> E;
        vector<vector<pair<int, int>>> adj(V);
        for (int j = 0; j < E; ++j) {
            int u, v, w;
            in >> u >> v >> w;
            adj[u].push_back({v, w});
            adj[v].push_back({u, w}); // undirected
        }

        vector<int> dist(V, 1e9);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        dist[0] = 0;
        pq.push({0, 0});
        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u]) continue;
            for (auto& edge : adj[u]) {
                int v = edge.first;
                int w = edge.second;
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }
        if (dist[V-1] == 1e9) distances.push_back(0);
        else distances.push_back(dist[V-1]);
    }

    mt19937 gen(42);
    uniform_int_distribution<int> dist(0, N - 1);

    vector<double> means(10000);
    for (int i = 0; i < 10000; ++i) {
        double sum = 0;
        for (int j = 0; j < N; ++j) {
            sum += distances[dist(gen)];
        }
        means[i] = sum / N;
    }

    sort(means.begin(), means.end());

    cout << fixed << setprecision(2);
    cout << "Lower: " << means[250] << ", Upper: " << means[9750] << endl;
    return 0;
}
"""
    cpp_file = "/tmp/reference_solver.cpp"
    exe_file = "/tmp/reference_solver"

    with open(cpp_file, "w") as f:
        f.write(cpp_code)

    subprocess.run(["g++", "-O2", cpp_file, "-o", exe_file], check=True)
    result = subprocess.run([exe_file], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_bootstrap_means_file():
    means_file = "/home/user/bootstrap_means.txt"
    assert os.path.exists(means_file), f"Missing file: {means_file}"

    with open(means_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 10000, f"Expected exactly 10000 lines in {means_file}, found {len(lines)}"

    # Verify they are numbers
    try:
        [float(line.strip()) for line in lines]
    except ValueError:
        pytest.fail(f"Not all lines in {means_file} are valid floats.")

def test_ci_result_file():
    ci_file = "/home/user/ci_result.txt"
    assert os.path.exists(ci_file), f"Missing file: {ci_file}"

    with open(ci_file, "r") as f:
        content = f.read().strip()

    expected_ci = get_expected_ci()
    assert content == expected_ci, f"Content of {ci_file} is incorrect. Expected '{expected_ci}', got '{content}'"

def test_distribution_plot_exists():
    plot_file = "/home/user/distribution.png"
    assert os.path.exists(plot_file), f"Missing file: {plot_file}"
    assert os.path.getsize(plot_file) > 0, f"File {plot_file} is empty"