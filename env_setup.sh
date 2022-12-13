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

# Testa se o anaconda e o pip estão instalados
if ! conda info | grep -qi 'active environment'; then
  echo -e "${VERMELHO}[ERROR] - O Anaconda não está instalado. Faça o download em: https://www.anaconda.com/products/distribution, instale e tente novamente.${SEM_COR}"
  exit 1
elif ! dpkg -l | grep -q python3-pip; then
  echo -e "${VERMELHO}[ERROR] - Um pacote necessário não está instalado. Instale o " python3-pip " e tente novamente.${SEM_COR}"
  exit 1
else
  echo -e "${VERDE}[INFO] - O sistema atende aos requisitos.${SEM_COR}"
fi

# Cria o ambiente conda
conda create -yq -n $ENV_NAME python=$PY_VER

# Testa se o ambiente conda foi criado e instala os pacotes
if conda env list | grep -q $ENV_NAME; then
  # Ativa o ambiente para a instalação dos pacotes
  source ~/anaconda3/etc/profile.d/conda.sh
  conda activate $ENV_NAME
  echo -e "${VERDE}[INFO] - Ambiente conda criado! Aguarde a instalação dos pacotes...${SEM_COR}"
  # Instala os pacotes
  for package in ${CONDA_PACKS[@]}; do
    pip -q install $package
  done
  echo -e "${VERDE}[INFO] - Pacotes instalados. Use o comando '${AMARELO}conda activate $ENV_NAME${VERDE}' para habilitar o ambiente criado.${SEM_COR}"
else
  echo -e "${VERMELHO}[ERROR] - Falha ao criar o ambiente conda.${SEM_COR}"
fi
