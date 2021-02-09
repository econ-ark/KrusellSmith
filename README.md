# KrusellSmith

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/econ-ark/KrusellSmith/HEAD)

This is a Replication of Krusell and Smith, 1998.

To reproduces all the results of the paper, you can

##### Use [nbreproduce](https://github.com/econ-ark/nbreproduce) (requires Docker to be installed on the machine).

```
# Clone this repository
$ git clone https://github.com/econ-ark/KrusellSmith

# Change working directory to KrusellSmith
$ cd KrusellSmith

# Install nbreproduce
$ pip install nbreproduce

# Reproduce all results using nbreproduce
$ nbreproduce
```

##### Install a local conda environment and execute the Jupyter notebook.

```
$ conda env create -f environment.yml
$ conda activate krusellsmith
# execute the script to create figures
$ cd Code/Python
$ ipython KrusellSmith.py
```

## References

Krusell, P., & Smith, Jr, A. A. (1998). Income and wealth heterogeneity in the macroeconomy. Journal of political Economy, 106(5), 867-896.
