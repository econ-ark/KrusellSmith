# requirements setup and mamba for faster install for env
source /opt/conda/etc/profile.d/conda.sh
mamba env create -qq -f environment.yml
conda activate krusellsmith

# execute the script to create figures
cd Code/Python
ipython KrusellSmith.py
