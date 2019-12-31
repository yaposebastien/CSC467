#!bin/bash

wget --no-check-certificate https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/anaconda3
echo "PATH=/opt/anaconda3/bin:$PATH" | sudo tee -a /etc/environment
source /etc/environment
conda install -c conda-forge notebook
