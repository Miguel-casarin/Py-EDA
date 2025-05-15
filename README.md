# Py-EAD
Um Electronic Design Automation (EDA) é um conjunto de ferramentas de software usadas para projetar, simular e verificar circuitos eletrônicos, como chips e placas, ele serve automatizar e agilizar o desenvolvimento de Hardware.

Nesse trabalho foi desenvolvido um protótipo de um simples EDA escrito em Python, que organiza as células por meio de uma tabeça Hash.
## Libs
-Matplotlib

-Tkinter

## Notação Big O de uma tabela Hash
Inserção, busca e remoção: no melhor e caso médio, têm complexidade O(1) (tempo constante), pois acessam diretamente o índice calculado pela função hash.

No pior caso, com muitas colisões mal resolvidas, pode chegar a O(n), onde n é o número de elementos. Isso ocorre quando todos os dados caem na mesma posição e são armazenados em uma lista ou estrutura encadeada.

## Descrevendo o Código
```python
LARGURA_TOTAL = 2500
ALTURA_LINHA = 504
NUM_LINHAS = 145
ARQUIVO_ENTRADA = 'exemplo_bookshelf.nodes'
```
Aqui e definido a tamanho das variáves que irão controlar a estrutura do circuito e o modo como a tabela Hash vai lidar com os dados


