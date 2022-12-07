#!/usr/bin/env bash

# Conda env name
ENV_NAME="env-proj1-393-py38"

# Packages
CONDA_PACKAGES=(
  scikit-learn==1.1.3
  scikit-image==0.19.3
  matplotlib==3.6.0
  pandas==1.5.1
  seaborn==0.12.1
  notebook==6.5.1
)

# Font colors
VERDE='\e[1;92m'
AMARELO='\e[1;93m'
SEM_COR='\e[0m'

# ----------------------------------------------------------------------------- #

conda create -yq -n $ENV_NAME python=3.8

for package in ${CONDA_PACKAGES[@]}; do
  conda install -yq -n $ENV_NAME -c conda-forge $package
done

echo -e "${VERDE}[INFO] - Ambiente conda configurado, para utilizar, use ${AMARELO}'conda activate $ENV_NAME'${VERDE}.${SEM_COR}"
