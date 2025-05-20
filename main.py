import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Carregar a imagem (substitua pelo caminho da sua imagem de satélite)
image = cv2.imread('imagem-teste.png')  ### coloque aqui o nome do arquivo da sua imagem
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Redimensionar para facilitar o processamento
image_resized = cv2.resize(image_rgb, (400, 400))

# Converter a imagem para um vetor 2D de pixels (cada pixel é uma linha com suas 3 cores RGB)
pixels = image_resized.reshape((-1, 3))

# Aplicando o K-means para segmentação
n_clusters = 4  # Vamos tentar 4 clusters para representar diferentes tipos de áreas
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(pixels)

# Prever os clusters para cada pixel
segmented_image = kmeans.predict(pixels)

# Reformatar a imagem segmentada para o formato original (resolução 400x400x3)
segmented_image = segmented_image.reshape(image_resized.shape[:2])

# Visualizar a imagem segmentada
plt.imshow(segmented_image, cmap='viridis')
plt.title('Imagem Segmentada - K-means')
plt.colorbar()
plt.show()

# Examinando as cores médias de cada cluster para identificar qual corresponde à área agrícola
cluster_centers = kmeans.cluster_centers_
print("Centros dos clusters (cores médias):")
for i, center in enumerate(cluster_centers):
    print(f"Cluster {i}: {center}")

# Identificando o cluster que mais provavelmente corresponde à área agrícola
# Aqui estamos assumindo que o cluster com a cor média mais próxima de tons verdes (relacionados à agricultura) é o relevante
agriculture_cluster = None
green_range = np.array([30, 80, 30])  # A faixa de verde para detectar áreas agrícolas

# Encontrar o cluster com cor mais próxima do verde (ajuste conforme necessário)
distances = np.linalg.norm(cluster_centers - green_range, axis=1)
agriculture_cluster = np.argmin(distances)

print(f'O cluster que corresponde à área agrícola é: {agriculture_cluster}')

# Criando a máscara para áreas agrícolas
agriculture_mask = (segmented_image == agriculture_cluster)

# Mostrar a máscara agrícola
plt.imshow(agriculture_mask, cmap='gray')
plt.title('Área Agrícola Identificada')
plt.show()

# Sobrepondo a máscara sobre a imagem original para uma visualização mais clara
highlighted_image = image_resized.copy()
highlighted_image[~agriculture_mask] = 0  # Apaga os pixels que não são agrícolas

plt.imshow(highlighted_image)
plt.title('Área Agrícola Sobreposta na Imagem Original')
plt.show()
