import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Carregar a imagem
image = cv2.imread('imagem-teste.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Dimensões da imagem original
img_alt, img_larg, canais = image_rgb.shape
tam_bloco = 400
contador = 0

# Imagens finais (vazias) para reconstrução
imagem_reconstruida = np.zeros_like(image_rgb)
segmentacao_global = np.zeros((img_alt, img_larg), dtype=np.uint8)
mascara_global = np.zeros((img_alt, img_larg), dtype=np.uint8)

for y in range(0, img_alt, tam_bloco):
    for x in range(0, img_larg, tam_bloco):
        bloco = image_rgb[y:min(y+tam_bloco, img_alt), x:min(x+tam_bloco, img_larg)]

        # Processamento
        pixels = bloco.reshape((-1, 3))
        kmeans = KMeans(n_clusters=4, random_state=42)
        kmeans.fit(pixels)
        segmented = kmeans.predict(pixels).reshape(bloco.shape[:2])

        # Cluster agrícola
        cluster_centers = kmeans.cluster_centers_
        green_range = np.array([30, 80, 30])
        distances = np.linalg.norm(cluster_centers - green_range, axis=1)
        agriculture_cluster = np.argmin(distances)
        mask = (segmented == agriculture_cluster)

        # Destacar área agrícola
        highlighted = bloco.copy()
        highlighted[~mask] = 0

        # Coordenadas reais do bloco
        altura_bloco, largura_bloco = highlighted.shape[:2]
        imagem_reconstruida[y:y+altura_bloco, x:x+largura_bloco] = highlighted
        segmentacao_global[y:y+altura_bloco, x:x+largura_bloco] = segmented
        mascara_global[y:y+altura_bloco, x:x+largura_bloco] = (mask * 255).astype(np.uint8)

        contador += 1

print(f'{contador} blocos processados.')

# Mostrar cada imagem em uma janela separada (uma por vez)

# 1. Segmentação com colormap viridis
plt.figure()
plt.imshow(segmentacao_global, cmap='viridis')
plt.title('Imagem Segmentada (K-means)')
plt.axis('off')
plt.show()

# 2. Máscara em preto e branco
plt.figure()
plt.imshow(mascara_global, cmap='gray')
plt.title('Máscara de Área Agrícola')
plt.axis('off')
plt.show()

# 3. Imagem original com áreas agrícolas destacadas
plt.figure()
plt.imshow(imagem_reconstruida)
plt.title('Áreas Agrícolas Destacadas')
plt.axis('off')
plt.show()
