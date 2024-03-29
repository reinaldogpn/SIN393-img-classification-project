# -*- coding: utf-8 -*-
"""projeto_sin393.ipynb

Automatically generated by Colaboratory.

# **Projeto Visão Computacional - Classificação de Imagens**

### **Preparando o ambiente**
"""

import os

import numpy as np

from skimage import transform, measure, util, color, filters, morphology
from sklearn import model_selection, neighbors, metrics, preprocessing

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

%matplotlib notebook

"""### **Parâmetros para reprodutibilidade**"""

random_state=393
np.random.seed(random_state)

"""### **Preparando o conjunto de dados**"""

# Define o caminho para o conjunto de dados completo
ds_path = 'data/mpeg7_4classes_aug_x8_work'

# Define o caminho para o conjunto de treino
train_path = ds_path + '/Train'

# Define uma lista com os nomes das classes
classes_list = os.listdir(train_path)

print(f'Classes: {classes_list}')

# Lista com as imagens no dataset de treino
train_image_list = []

# Lista com os rótulos das imagens no dataset de treino
train_label_list = []

# Lista com os nomes das imagens
train_filename_list = []

# Percorre as classes do dataset
for classe in classes_list:

    # Listagem de todas as imagens na pasta daquela classe
    filename_list_tmp = os.listdir(os.path.join(train_path, classe))

    for filename in filename_list_tmp:

        # Carrega a imagem
        img_tmp = plt.imread(os.path.join(train_path, classe, filename))
        
        # Redimensiona a imagem para 164 x 164 pixels
        img_tmp = transform.resize(img_tmp, (164, 164), anti_aliasing=True)
        
        # Adiciona a imagem a lista de imagens
        train_image_list.append(img_tmp)
        
        # Adiciona o rótulo da imagem à lista de rótulos
        train_label_list.append(classe)
        
        # Adiciona o nome da imagem à uma lista (para fins de visualização)
        train_filename_list.append(filename)

# Conversão dos nomes das classes para índices numéricos
_, _, label_list_train_idx = np.unique(train_label_list, return_index=True, return_inverse=True)

"""### **Plotando as imagens**"""

image_list_temp = []
filename_list_temp = []

# Seleciona 6 imagens de cada uma das 4 classes
for i in range(4):
    image_list_temp += [train_image_list[j] for j in np.where(label_list_train_idx==i)[0][:6]]
    filename_list_temp += [train_filename_list[j] for j in np.where(label_list_train_idx==i)[0][:6]]

fig, ax  = plt.subplots(4, 6, figsize=(9, 5))

for i, (image, filename) in enumerate(zip(image_list_temp, filename_list_temp)):
    ax[i//6, i%6].imshow(image, cmap='gray')
    ax[i//6, i%6].set_title(str(filename))

fig.tight_layout()
plt.show()

"""### **Extração de características**"""

# Características que serão extraídas
features = ['area', 'area_convex', 'extent', 'major_axis', 'minor_axis', 'solidity']

def FeatureXtract(img_list, lbl_list):
    
    # Matriz que irá armazenar as características das imagens
    feature_mat = []
    
    # Lista que irá armazenar as novas imagens
    new_img_list = []
    
    # Lista que irá armazenar os rótulos das imagens
    list_label = []

    for i, (image, label) in enumerate(zip(img_list, lbl_list)):

        # Adiciona o rótulos (label) da imagem à lista
        list_label.append(label)

        # Remove objetos na imagem com menos de N pixels
        new_image = morphology.remove_small_objects(image.astype(bool), 80)

        # Adiciona a imagem modificada à lista
        new_img_list.append(new_image)

        # Calcula a imagem de rótulos
        img_label = measure.label(new_image)

        # Calcula uma lista de propriedades (caracteristicas) dos objetos na imagem
        props = measure.regionprops(img_label)
        
        if len(props) != 1:
            print(f'ERRO de segmentação: {len(props)}')
            continue

        # Itera pelas propriedades computadas
        for prop in props:

            # Prop. 0: Area
            area = prop.area

            # Prop. 1: Area Convexa
            area_convex = prop.area_convex

            # Prop. 2: Extensão
            extent = prop.extent

            # Prop. 3: Maior eixo
            major_axis = prop.major_axis_length

            # Prop. 4: Menor eixo
            minor_axis = prop.minor_axis_length 

            # Prop. 5: Solidez
            solidity = prop.solidity

            # Monta o vetor de caracteristicas deste objeto
            feature_list = [area, area_convex, extent, major_axis, minor_axis, solidity]

        # Adiciona as caracteristicas desta imagem na matriz de caracteristicas
        feature_mat.append(feature_list)
    
    # Retorna a matriz de características
    return feature_mat

# Realiza a extração de características no conjunto de treino
train_feature_mat = FeatureXtract(train_image_list, train_label_list)

# Converte a lista de caracteristicas para um arranjo NumPy
train_feature_map = np.array(train_feature_mat)

# Imprime a matriz de caracteristica
with np.printoptions(precision=4, suppress=True):
    print(train_feature_map)

"""### **Plotando as caracteristicas computadas**"""

df = pd.DataFrame(train_feature_map, columns=features)

df['class'] = train_label_list

display(df)

g = sns.PairGrid(df, hue='class', vars=features)
g.fig.set_size_inches(8, 8)
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)
g.add_legend()

"""### **Validação cruzada (Hold-out)**"""

# Separa o conjunto de dados em 'train_feature_map', de acordo com 'train_label_list'. 
# 30% das imagens vão para o conjunto de validação.
X_train, X_val, y_train, y_val = model_selection.train_test_split(train_feature_map, 
                                                                  train_label_list, 
                                                                  test_size=0.3,
                                                                  stratify=train_label_list,
                                                                  random_state=random_state)

"""### **Normalização das características do novo conjunto de treinamento**"""

# Transformada Normal de Caracteristicas (Sklearn)
scaler = preprocessing.StandardScaler().fit(X_train)
with np.printoptions(precision=4, suppress=True):
    print(f'Média:  \t {np.array(scaler.mean_)}')
    print(f'Desv. pad.: \t {np.array(scaler.scale_)}')

X_train_norm = scaler.transform(X_train)
X_val_norm = scaler.transform(X_val)

with np.printoptions(precision=4, suppress=True):
    print(f'Treino: \t {X_train_norm.mean():.4f} ± {X_train_norm.std():.4f}')
    print(f'Validação: \t {X_val_norm.mean():.4f} ± {X_val_norm.std():.4f}')

"""### **Classificação através do KNN, buscando o melhor valor de K**"""

k_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Lista com as acurácias de treino
acc_train_list = []

# Lista com as acurácias de validação
acc_val_list = []

for k_ in k_list:
    
    # Constrói um classificador K-NN K = k_
    clf = neighbors.KNeighborsClassifier(n_neighbors=k_)

    # Treinando o classificador
    clf.fit(X_train_norm, y_train)

    # Testando o classificador (usando o conjunto de validação)
    pred = clf.predict(X_val_norm)
    acc_val = metrics.accuracy_score(y_val, pred)
    
    acc_val_list.append(acc_val)
    
    # Testando o classificador (usando o conjunto de treino) para fins de comparação
    pred_train = clf.predict(X_train_norm)
    acc_train = metrics.accuracy_score(y_train, pred_train)
    
    acc_train_list.append(acc_train)

plt.figure(figsize=(9, 6))

plt.plot(k_list, acc_train_list, 'o', color='blue', label='treino')
plt.plot(k_list, acc_val_list, 'x', color='red', label='validação')
plt.xlabel("Valor de 'k'")
plt.ylabel("Acurácia")
plt.legend(loc='best')

plt.show()

print('k \t acc. treino \t acc. val')
print('----------------------------')
for k_, acc_t, acc_v in zip(k_list, acc_train_list, acc_val_list):
    print(f'{k_} \t {acc_t:.4f} \t {acc_v:.4f}')

k_best = k_list[np.argmax(acc_val_list)]
print(f'\nMelhor \'k\': {k_best} ({np.max(acc_val_list):.4f} acc.)')

"""### **Avaliação do modelo**"""

# Acertos
acertos = y_val == pred

print('\n Predição:')
print(pred)
print('\nReal:')
print(y_val)
print('\nAcerto/Erro:')
print(acertos.astype(int))

"""### **Matriz de confusão e o relatório de treinamento (VALIDAÇÃO)**"""

print('\nMatriz de confusão:')
print(metrics.confusion_matrix(y_val, pred))

print('\nRelatório de classificação:')
print(metrics.classification_report(y_val, pred))

print('\nAcurácia:')
print(f'{(acc_val*100):.4f}%')

"""## **Validação do modelo (conjunto de testes)**

### **Carregando o conjunto de teste**
"""

#ds_path = 'data/mpeg7_4classes_aug_x8_work'

test_path = ds_path + '/Test'

classes_list = os.listdir(test_path)

print(f'Classes: {classes_list}')

test_image_list = []
test_label_list = []
test_filename_list = []

for classe in classes_list:

    filename_list_tmp = os.listdir(os.path.join(test_path, classe))

    for filename in filename_list_tmp:

        img_tmp = plt.imread(os.path.join(test_path, classe, filename))
        img_tmp = transform.resize(img_tmp, (164, 164), anti_aliasing=True)
        test_image_list.append(img_tmp)
        test_label_list.append(classe)
        test_filename_list.append(filename)

# Conversão dos nomes das classes para índices numéricos
_, _, test_label_list_idx = np.unique(test_label_list, return_index=True, return_inverse=True)
print(test_label_list_idx)

"""### **Extraindo as características do conjunto de testes**"""

# Realiza a extração de características no conjunto de teste
test_feature_mat = FeatureXtract(test_image_list, test_label_list)

# Converte a lista de caracteristicas para um arranjo NumPy
test_feature_map = np.array(test_feature_mat)

"""### **Plotando as características normalizadas**"""

df_norm = pd.DataFrame(test_feature_map, columns=features)

df_norm['class'] = test_label_list
print(df_norm)

# Imprime a matriz de caracteristica
with np.printoptions(precision=4, suppress=True):
    print(test_feature_map)

"""### **Normalizando as caracteristicas**"""

X_test = test_feature_map[0:len(test_image_list),:]

# Transformada Normal de Caracteristicas (Sklearn)
scaler = preprocessing.StandardScaler().fit(X_test)
with np.printoptions(precision=4, suppress=True):
    print(f'Média:  \t {np.array(scaler.mean_)}')
    print(f'Desv. pad.: \t {np.array(scaler.scale_)}')

X_test_norm = scaler.transform(X_test)
print(X_test_norm)

"""### **Nova classificação do modelo utilizando o KNN e o conjunto de testes**"""

# Classificação utilizando o melhor valor de k (k_best)
clf = neighbors.KNeighborsClassifier(n_neighbors=k_best)

# Treinando o classificador
clf.fit(X_train_norm, y_train)

# Testando o classificador
pred = clf.predict(X_test_norm)
acc_test = metrics.accuracy_score(test_label_list, pred)

"""### **Matriz de confusão e relatório de classificação (TESTE)**"""

print('\nMatriz de confusão:')
print(metrics.confusion_matrix(test_label_list, pred))

print('\nRelatório de classificação:')
print(metrics.classification_report(test_label_list, pred))

print('\nAcurácia:')
print(f'{(acc_test*100):.4f}%')