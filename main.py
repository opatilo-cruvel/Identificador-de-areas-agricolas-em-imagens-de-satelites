from mpi4py import MPI
import os
from processamento import processar_imagem
import glob
from time import time
from concurrent.futures import ThreadPoolExecutor

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Caminho das imagens
pasta_imagens = "imgs"

if not os.path.exists(pasta_imagens):
    print(f"Erro: A pasta '{pasta_imagens}' não foi encontrada.")
    exit(1)

# Obter todos os arquivos .png
arquivos = sorted(glob.glob(os.path.join(pasta_imagens, "*.png")))

if len(arquivos) == 0:
    print("Erro: Nenhuma imagem '.png' encontrada.")
    exit(1)

# Dividir imagens em blocos contíguos
def dividir_blocos(lista, n_blocos):
    tamanho = len(lista)
    bloco = tamanho // n_blocos
    resto = tamanho % n_blocos
    return [lista[i*bloco + min(i, resto):(i+1)*bloco + min(i+1, resto)] for i in range(n_blocos)]

imagens_divididas = dividir_blocos(arquivos, size)
imagens_do_processo = imagens_divididas[rank]

# Criar pasta para resultados deste processo
resultados_pasta = f"resultados/rank_{rank}"
os.makedirs(resultados_pasta, exist_ok=True)

# Definir máximo de threads por processo (ajuste conforme CPU/memória)
MAX_THREADS = 3

inicio = time()

def worker(caminho_img):
    nome_arquivo = os.path.basename(caminho_img)
    saida_path = os.path.join(resultados_pasta, nome_arquivo)
    processar_imagem(caminho_img, saida_path)

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    executor.map(worker, imagens_do_processo)

fim = time()
tempo_total = fim - inicio
total_imgs = len(imagens_do_processo)

# Enviar dados para o processo 0
tempos = comm.gather(tempo_total, root=0)
quantidades = comm.gather(total_imgs, root=0)

if rank == 0:
    print("\n=== RESUMO DA EXECUÇÃO ===")
    total_geral = 0
    tempo_total_geral = 0
    for i in range(size):
        print(f"Rank {i}: {quantidades[i]} imagens em {tempos[i]:.2f} segundos")
        total_geral += quantidades[i]
        tempo_total_geral += tempos[i]
    print(f"\nTotal: {total_geral} imagens processadas")
    print(f"Tempo médio por imagem: {tempo_total_geral / total_geral:.4f} segundos\n")