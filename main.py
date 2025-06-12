from mpi4py import MPI
import cv2
import numpy as np
from sklearn.cluster import KMeans

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Apenas o processo mestre carrega a imagem
if rank == 0:
    image = cv2.imread('imagem-teste.png')
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_alt, img_larg, canais = image_rgb.shape
else:
    image_rgb = None
    img_alt = img_larg = canais = 0

# Broadcast das dimensões
img_alt = comm.bcast(img_alt if rank == 0 else None, root=0)
img_larg = comm.bcast(img_larg if rank == 0 else None, root=0)

tam_bloco = 400
blocos = []

# O processo mestre cria a lista de blocos a serem processados
if rank == 0:
    for y in range(0, img_alt, tam_bloco):
        for x in range(0, img_larg, tam_bloco):
            blocos.append((y, x))

# Divide os blocos entre os processos
blocos_locais = np.array_split(blocos, size)[rank]

resultados = []

if rank == 0:
    print(f"Iniciando com {size} processos MPI...")

for y, x in blocos_locais:
    bloco = image_rgb[y:min(y+tam_bloco, img_alt), x:min(x+tam_bloco, img_larg)]
    pixels = bloco.reshape((-1, 3))
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    kmeans.fit(pixels)
    segmented = kmeans.predict(pixels).reshape(bloco.shape[:2])

    cluster_centers = kmeans.cluster_centers_
    green_range = np.array([30, 80, 30])
    distances = np.linalg.norm(cluster_centers - green_range, axis=1)
    agriculture_cluster = np.argmin(distances)
    mask = (segmented == agriculture_cluster)

    highlighted = bloco.copy()
    highlighted[~mask] = 0

    resultados.append((y, x, highlighted, segmented, (mask * 255).astype(np.uint8)))

# Recolher os resultados no processo 0
todos_resultados = comm.gather(resultados, root=0)

# Processo 0 reconstrói as imagens
if rank == 0:
    imagem_reconstruida = np.zeros_like(image_rgb)
    segmentacao_global = np.zeros((img_alt, img_larg), dtype=np.uint8)
    mascara_global = np.zeros((img_alt, img_larg), dtype=np.uint8)

    for resultado_processo in todos_resultados:
        for y, x, highlighted, segmented, mask in resultado_processo:
            altura_bloco, largura_bloco = highlighted.shape[:2]
            imagem_reconstruida[y:y+altura_bloco, x:x+largura_bloco] = highlighted
            segmentacao_global[y:y+altura_bloco, x:x+largura_bloco] = segmented
            mascara_global[y:y+altura_bloco, x:x+largura_bloco] = mask

    import matplotlib.pyplot as plt

    plt.figure()
    plt.imshow(segmentacao_global, cmap='viridis')
    plt.title('Imagem Segmentada (K-means)')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(mascara_global, cmap='gray')
    plt.title('Máscara de Área Agrícola')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(imagem_reconstruida)
    plt.title('Áreas Agrícolas Destacadas')
    plt.axis('off')
    plt.show()
