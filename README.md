# Identificador-de-areas-agricolas-em-imagens-de-satelites

## Descrição

Este projeto acadêmico visa **identificar áreas agrícolas em imagens de satélite** utilizando técnicas de **segmentação de imagens** com o algoritmo **K-means**. O foco principal está em **paralelizar o processo de segmentação**, para permitir o processamento eficiente de grandes volumes de imagens de satélite, especialmente imagens no formato **.tiff**, comuns em dados geoespaciais.

## Desafio

O **desafio principal** proposto pelo professor é **paralelizar o processo de segmentação**, permitindo que várias imagens de satélite sejam processadas de forma mais eficiente utilizando múltiplos núcleos de processamento. A segmentação é feita através do algoritmo **K-means**, que agrupa os pixels de uma imagem em clusters com base em suas cores, e a identificação das áreas agrícolas é feita a partir dos clusters mais próximos dos tons de verde.

## Funcionalidades

- **Pré-processamento de Imagens**: Converte imagens de satélite no formato `.tiff` para uma representação manipulável (matriz RGB) para segmentação.
- **Segmentação com K-means**: Aplica o algoritmo K-means para segmentar a imagem em diferentes clusters e identificar áreas agrícolas.
- **Visualização**: Gera visualizações para mostrar as áreas agrícolas detectadas, sobrepondo a máscara segmentada sobre a imagem original.
- **Paralelização**: O processo de segmentação será otimizado para ser executado de maneira paralela, aproveitando múltiplos núcleos de processamento.

## Tecnologias Utilizadas

- **Python**: Linguagem principal para o processamento e análise.
- **OpenCV**: Biblioteca para carregamento, manipulação e visualização de imagens.
- **Scikit-learn**: Biblioteca para aplicar o algoritmo de segmentação K-means.
- **Matplotlib**: Biblioteca para visualização das imagens e segmentação.
- **Multiprocessing/Dask**: Para paralelização do processo de segmentação.

## Como Rodar o Projeto

### Pré-requisitos

1. **Python 3.x** instalado.
2. As bibliotecas necessárias podem ser instaladas com o `pip`:

```bash
pip install opencv-python numpy matplotlib scikit-learn dask
```

### Para Executar o código

1. Adicione a imagem na pasta do projeto
2. Na linha 7 do arquivo main.py, coloque o nome do arquivo de imagem que vai ser processado
`image = cv2.imread('imagem-teste.png')`
3. rode o comando `python main.py` no terminal para executar o código
