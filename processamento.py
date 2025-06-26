from PIL import Image
import numpy as np
import cv2
from sklearn.cluster import KMeans
from concurrent.futures import ThreadPoolExecutor

Image.MAX_IMAGE_PIXELS = None

BLOCO_TAM = 2000
MAX_THREADS_BLOCOS = 1  # Máximo de threads por imagem

def redimensionar_imagem_em_memoria(caminho_imagem, max_dim=30000):
    try:
        img = Image.open(caminho_imagem)
        w, h = img.size

        if h > max_dim or w > max_dim:
            scale_factor = max_dim / float(max(h, w))
            new_w, new_h = int(w * scale_factor), int(h * scale_factor)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        return np.array(img.convert("RGB"))
    except Exception as e:
        print(f"[ERRO] Falha ao redimensionar imagem '{caminho_imagem}': {e}")
        return None

def processar_bloco(bloco_rgb, x_ini, y_ini, resultado_shape):
    try:
        h, w = bloco_rgb.shape[:2]
        bloco_red = cv2.resize(bloco_rgb, (min(w, 800), min(h, 800)))
        pixels = bloco_red.reshape((-1, 3))

        kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
        kmeans.fit(pixels)

        labels = kmeans.labels_.reshape(bloco_red.shape[:2])
        centers = kmeans.cluster_centers_
        verde_idx = np.argmax(centers[:, 1])  # canal G

        bloco_segmentado = np.zeros_like(bloco_red)
        for i in range(3):
            cor = (0, 255, 0) if i == verde_idx else (40, 40, 40)
            bloco_segmentado[labels == i] = cor

        # Redimensionar de volta ao tamanho original do bloco (pode ser menor que 2000x2000)
        bloco_final = cv2.resize(bloco_segmentado, (w, h), interpolation=cv2.INTER_NEAREST)
        return (y_ini, x_ini, bloco_final)

    except Exception as e:
        print(f"[ERRO] Erro ao processar bloco em ({x_ini}, {y_ini}): {e}")
        return (y_ini, x_ini, np.zeros((resultado_shape[0], resultado_shape[1], 3), dtype=np.uint8))

def processar_imagem(caminho_imagem, caminho_saida):
    image_rgb = redimensionar_imagem_em_memoria(caminho_imagem)

    if image_rgb is None:
        return

    altura, largura = image_rgb.shape[:2]
    resultado_final = np.zeros((altura, largura, 3), dtype=np.uint8)

    blocos_tarefas = []

    # Dividir a imagem em blocos de 2000x2000
    for y in range(0, altura, BLOCO_TAM):
        for x in range(0, largura, BLOCO_TAM):
            bloco = image_rgb[y:y+BLOCO_TAM, x:x+BLOCO_TAM]
            blocos_tarefas.append((bloco, x, y, bloco.shape[:2]))

    # Processar blocos com threads (limite: MAX_THREADS_BLOCOS simultâneas)
    with ThreadPoolExecutor(max_workers=MAX_THREADS_BLOCOS) as executor:
        futures = [
            executor.submit(processar_bloco, bloco, x_ini, y_ini, shape)
            for bloco, x_ini, y_ini, shape in blocos_tarefas
        ]

        for future in futures:
            y, x, bloco_processado = future.result()
            h, w = bloco_processado.shape[:2]
            resultado_final[y:y+h, x:x+w] = bloco_processado

    # Salvar imagem segmentada
    cv2.imwrite(caminho_saida, resultado_final)