import rasterio
import numpy as np
import matplotlib.pyplot as plt

def normalize_band(band, low=2, high=98):
    p_low, p_high = np.percentile(band, (low, high))
    return np.clip((band - p_low) / (p_high - p_low), 0, 1)

# Caminho base da imagem
base_path = "teste_landcast/LT05_L2SP_219068_20110912_20200820_02_T1_SR_"

# Lista de bandas que vamos usar (B1, B2, B3, B4, B5, B7)
band_ids = ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']
bands = []

# Abrir e normalizar cada banda
for b in band_ids:
    with rasterio.open(base_path + b + ".TIF") as src:
        band = src.read(1).astype(np.float32)
        norm_band = normalize_band(band)
        bands.append(norm_band)

# Empilhar todas as bandas em um único array (Alt, Larg, 6)
multi_band_image = np.stack(bands, axis=-1)

print("Shape da imagem multibanda:", multi_band_image.shape)

# (Opcional) Visualização usando bandas RGB tradicionais (B3, B2, B1)
# índice 2 = B3 (Red), 1 = B2 (Green), 0 = B1 (Blue)
rgb_image = np.stack([bands[2], bands[1], bands[0]], axis=-1)

plt.figure(figsize=(8, 8))
plt.imshow(rgb_image)
plt.title("Visualização RGB (B3-B2-B1) com Stretching")
plt.axis('off')
plt.show()
