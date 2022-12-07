#!/usr/bin/env bash

# Nome do ambiente conda
ENV_NAME="env-proj1-393-py38"

# Versão do python
PY_VER=3.8

# Pacotes que serão instalados
CONDA_PACKS=(
  scikit-learn==1.1.3
  scikit-image==0.19.3
  matplotlib==3.6.0
  pandas==1.5.1
  seaborn==0.12.1
  notebook==6.5.1
)

# Cores de fonte
VERDE='\e[1;92m'
AMARELO='\e[1;93m'
VERMELHO='\e[1;91m'
SEM_COR='\e[0m'

# ----------------------------------------------------------------------------- #

# Atualiza o conda
# conda update -n base -c defaults conda

# Cria o ambiente conda
conda create -yq -n $ENV_NAME python=$PY_VER

# Instala os pacotes
for package in ${CONDA_PACKS[@]}; do
  conda install -yq -n $ENV_NAME -c conda-forge $package
done

# Testa se o ambiente conda foi criado
if conda env list | grep $ENV_NAME; then
  echo -e "${VERDE}[INFO] - Ambiente conda configurado. Para utilizar, use o comando: ${AMARELO}conda activate $ENV_NAME.${SEM_COR}"
else
  echo -e "${VERMELHO}[ERROR] - Falha ao criar o ambiente conda.${SEM_COR}"
fi
