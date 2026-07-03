apt-get update && apt-get install -y python3 python3-pip python3-dev g++
    pip3 install --no-cache-dir pytest numpy pandas scikit-learn pybind11

    mkdir -p /app/data
    mkdir -p /app/fastpca-1.2

    # Generate data
    cat << 'EOF' > /tmp/generate_data.py
import os
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=2500, n_features=500, n_informative=15, n_redundant=10, random_state=42, class_sep=1.5)
X[:, :15] += 0.5 

df_train = pd.DataFrame(X[:1500], columns=[f'feature_{i}' for i in range(500)])
df_train['target'] = y[:1500]
df_train.to_csv('/app/data/train.csv', index=False)

df_test = pd.DataFrame(X[1500:], columns=[f'feature_{i}' for i in range(500)])
df_test.to_csv('/app/data/test.csv', index=False)

df_test_labels = pd.DataFrame({'target': y[1500:]})
df_test_labels.to_csv('/app/data/test_labels.csv', index=False)
EOF
    python3 /tmp/generate_data.py

    # Create fastpca files
    cat << 'EOF' > /app/fastpca-1.2/setup.py
from setuptools import setup, Extension
import pybind11
import numpy

ext_modules = [
    Extension(
        'fastpca',
        ['fastpca.cpp'],
        include_dirs=[], # BUG: missing pybind11 and numpy includes
        language='c++'
    ),
]

setup(
    name='fastpca',
    version='1.2',
    ext_modules=ext_modules,
)
EOF

    cat << 'EOF' > /app/fastpca-1.2/fastpca.cpp
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>

namespace py = pybind11;

py::array_t<double> reduce_dimensions(py::array_t<double> input, int n_components) {
    auto buf = input.request();
    double *ptr = static_cast<double *>(buf.ptr);
    int n_samples = buf.shape[0];
    int n_features = buf.shape[1];

    // Dummy PCA: just return the first n_components (since make_classification puts informative ones first)
    auto result = py::array_t<double>({n_samples, n_components});
    auto res_buf = result.request();
    double *res_ptr = static_cast<double *>(res_buf.ptr);

    for (int i = 0; i < n_samples; ++i) {
        for (int j = 0; j < n_components; ++j) {
            res_ptr[i * n_components + j] = ptr[i * n_features + j];
        }
    }
    return result;
}

PYBIND11_MODULE(fastpca, m) {
    m.def("reduce_dimensions", &reduce_dimensions, "Dummy dimensionality reduction");
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app