import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk 

LARGURA_TOTAL = 2500
ALTURA_LINHA = 504
NUM_LINHAS = 145
ARQUIVO_ENTRADA = 'exemplo_bookshelf.nodes'

class TabelaHash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela =[[] for _ in range(tamanho)]
    
    def hash(self, chave):
        return sum(ord(c) for c in chave) % self.tamanho
    
    def inserir(self, chave, valor):
        indice = self.hash(chave)
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                self.tabela[indice][i] = (chave, valor)
                return
        self.tabela[indice].append((chave, valor))

    def buscar(self, chave):
        indice = self.hash(chave)
        for k, v in self.tabela[indice]:
            if k == chave:
                return v
        return None
    
    def remover(self, chave):
        indice = self.hash(chave)
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                del self.tabela[indice][i]
                return True
        return False
    
class Organizador:
    def __init__(self, largura_l, altura_l, num_linhas):
        self.largura_l = largura_l
        self.altura_l = altura_l
        self.num_l = num_linhas
        self.linhas = [0.0] * num_linhas  
        self.espacos_livres = [[] for _ in range(num_linhas)] 
        self.tabela = TabelaHash(2000)    # hash por ID da célula

    def alocar_celula(self, id_celula, largura, altura, modo='legalizado'):
        if modo == 'randon':
            return self.alocar_celula_random(id_celula, largura, altura)

        for i in range(self.num_l):
            # Tenta usar espaços livres
            for j, (inicio, tam_livre) in enumerate(self.espacos_livres[i]):
                if largura <= tam_livre:
                    x = inicio
                    self.tabela.inserir(id_celula, (i, x))
                    # Atualiza ou remove o espaço livre usado
                    if largura == tam_livre:
                        self.espacos_livres[i].pop(j)
                    else:
                        self.espacos_livres[i][j] = (inicio + largura, tam_livre - largura)
                    return (i, x)

            # Se não houver espaço livre adequado, aloca ao final da linha
            if self.linhas[i] + largura <= self.largura_l:
                x = self.linhas[i]
                self.tabela.inserir(id_celula, (i, x))
                self.linhas[i] += largura
                return (i, x)
        return None


    
    def alocar_celula_random(self, id_celula, largura, altura):
        import random
        linhas_disponiveis = list(range(self.num_l))
        random.shuffle(linhas_disponiveis)

        for i in linhas_disponiveis:
            if self.linhas[i] + largura <= self.largura_l:
                x = self.linhas[i]
                self.tabela.inserir(id_celula, (i, x))
                self.linhas[i] += largura
                return (i, x)
        return None

    def calcular_ocupacao(self):
        area_total = self.largura_l * self.altura_l * self.num_l
        area_ocupada = 0.0

        for i in range(self.num_l):
            area_ocupada += self.linhas[i] * self.altura_l
        return (area_ocupada / area_total) * 100  

class GerarImagem:
    def __init__(self, largura_total, altura_linha, num_linhas):
        self.largura_total = largura_total
        self.altura_linha = altura_linha
        self.num_linhas = num_linhas

    def desenhar(self, celulas_alocadas):
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, self.largura_total)
        ax.set_ylim(0, self.altura_linha * self.num_linhas)
        
        for cel in celulas_alocadas:
            x = cel['x']
            y = cel['linha'] * self.altura_linha
            largura = cel['largura']
            altura = cel['altura']
            rect = patches.Rectangle(
                (x, y), largura, altura,
                linewidth=1, edgecolor='black', facecolor='red', alpha=0.7
            )
            ax.add_patch(rect)
            ax.text(x + largura / 2, y + altura / 2, cel['id'],
                    ha='center', va='center', fontsize=6, color='white')

        for i in range(self.num_linhas + 1):
            y = i * self.altura_linha
            ax.hlines(y, 0, self.largura_total, colors='gray', linewidth=0.5, linestyles='--', alpha=0.7)

        ax.grid(axis='y', linestyle='--', linewidth=0.5)

        plt.tight_layout()
        plt.show()

def ler_celulas(caminho):
    celulas = []
    with open(caminho, 'r') as f:
        for i, linha in enumerate(f, start=1):
            linha = linha.strip()
            if not linha or linha.startswith('#') or ':' in linha:
                continue
            partes = linha.split()
            if len(partes) != 3:
                print(f"[Linha {i}] Ignorada (formato inválido): {linha}")
                continue
            if not (partes[1].replace('.', '', 1).isdigit() and partes[2].replace('.', '', 1).isdigit()):
                print(f"[Linha {i}] Ignorada (valores não numéricos): {linha}")
                continue
            id_celula = partes[0]
            largura = float(partes[1])
            altura = float(partes[2])
            celulas.append({'id': id_celula, 'largura': largura, 'altura': altura})
    return celulas

def alocar_celulas(organizador, celulas):
    celulas_alocadas = []
    for cel in celulas:
        pos = organizador.alocar_celula(cel['id'], cel['largura'], cel['altura'])
        if pos is not None:
            linha_aloc, x_aloc = pos
            celulas_alocadas.append({'id': cel['id'], 'x': x_aloc, 'linha': linha_aloc, 'largura': cel['largura'], 'altura': cel['altura']})
        else:
            print(f"Não foi possível alocar célula {cel['id']} (largura={cel['largura']})")
    return celulas_alocadas

class InterfaceTk:
    def __init__(self, master, organizador, celulas_alocadas, largura_total, altura_linha, num_linhas):
        self.master = master
        self.master.title("EDA Com Hash")
        self.master.geometry("800x650")

        self.organizador = organizador
        self.celulas_alocadas = celulas_alocadas
        self.largura_total = largura_total
        self.altura_linha = altura_linha
        self.num_linhas = num_linhas

        self.b_imagem = tk.Button(master, text="GERAR IMAGEM", command=self.gerar_imagem)
        self.b_imagem.pack(pady=10)

        self.label_nova = tk.Label(master, text="Inserir nova célula:")
        self.label_nova.pack(pady=10)

        self.label_id = tk.Label(master, text="ID:")
        self.label_id.pack()
        self.entrada_id = tk.Entry(master)
        self.entrada_id.pack()

        self.label_largura = tk.Label(master, text="Largura:")
        self.label_largura.pack()
        self.entrada_largura = tk.Entry(master)
        self.entrada_largura.pack()

        self.label_modo = tk.Label(master, text="Modo de alocação:")
        self.label_modo.pack()

        self.modos = ["legalizado", "randon"]
        self.modo_selecionado = tk.StringVar(master)
        self.modo_selecionado.set(self.modos[0])  # Default: "legal"
        self.menu_modo = tk.OptionMenu(master, self.modo_selecionado, *self.modos)
        self.menu_modo.pack(pady=5)

        self.botao_inserir = tk.Button(master, text="INSERIR CÉLULA", command=self.inserir_celula)
        self.botao_inserir.pack(pady=10)

        self.msg_insercao = tk.Label(master, text="", fg="blue")
        self.msg_insercao.pack()

        self.label_busca = tk.Label(master, text="Buscar célula por ID:")
        self.label_busca.pack()

        self.entrada_busca = tk.Entry(master)
        self.entrada_busca.pack(pady=5)

        self.botao_buscar = tk.Button(master, text="BUSCAR", command=self.buscar_celula)
        self.botao_buscar.pack(pady=5)

        self.resultado_busca = tk.Label(master, text="", fg="blue")
        self.resultado_busca.pack()

        self.m_remover = tk.Label(master, text="Escolha a célula que deseja remover")
        self.m_remover.pack(pady=5)
        self.m_remover.pack(padx=(1, 150))

        self.opcoes = [cel['id'] for cel in celulas_alocadas]
        self.selecionado = tk.StringVar(master)
        if self.opcoes:
            self.selecionado.set(self.opcoes[0])
        else:
            self.selecionado.set('')

        self.menu = tk.OptionMenu(master, self.selecionado, *self.opcoes)
        self.menu.pack(pady=10)

        self.b_remover = tk.Button(master, text="REMOVER CÉLULA", command=self.remover_celula)
        self.b_remover.pack(pady=10)

        self.status_ocupacao = tk.Label(master, text="", fg="darkgreen")
        self.status_ocupacao.pack(pady=5)
        self.atualizar_ocupacao()

    def atualizar_ocupacao(self):
        ocupacao = self.organizador.calcular_ocupacao()
        self.status_ocupacao.config(text=f"Percentual de ocupação: {ocupacao:.2f}%")

    def gerar_imagem(self):
        imagem = GerarImagem(self.largura_total, self.altura_linha, self.num_linhas)
        imagem.desenhar(self.celulas_alocadas)
    
    def inserir_celula(self):
        id_novo = self.entrada_id.get().strip()
        largura_txt = self.entrada_largura.get().strip()

        if self.organizador.tabela.buscar(id_novo) is not None:
            self.msg_insercao.config(text="ID já utilizado.", fg="red")
            return

        if not id_novo or not largura_txt.replace('.', '', 1).isdigit():
            self.msg_insercao.config(text="Entrada inválida.", fg="red")
            return

        largura = float(largura_txt)
        altura = float(self.altura_linha)

        modo = self.modo_selecionado.get()

        pos = self.organizador.alocar_celula(id_novo, largura, altura, modo=modo)
        if pos is not None:
            linha_aloc, x_aloc = pos
            nova_celula = {
                'id': id_novo,
                'x': x_aloc,
                'linha': linha_aloc,
                'largura': largura,
                'altura': altura
            }
            self.celulas_alocadas.append(nova_celula)

            self.opcoes.append(id_novo)
            self.menu['menu'].add_command(label=id_novo, command=lambda v=id_novo: self.selecionado.set(v))
            self.selecionado.set(id_novo)

            self.msg_insercao.config(
                text=f"Célula '{id_novo}' inserida (modo: {modo}) na linha {linha_aloc}, X={x_aloc}",
                fg="green"
            )
        else:
            self.msg_insercao.config(text=f"Não foi possível alocar a célula '{id_novo}'", fg="red")

        self.atualizar_ocupacao()

    def buscar_celula(self):
        id_celula = self.entrada_busca.get().strip()
        if not id_celula:
            self.resultado_busca.config(text="Digite um ID válido.", fg="red")
            return

        pos = self.organizador.tabela.buscar(id_celula)
        if pos is not None:
            linha, x = pos
            self.resultado_busca.config(
                text=f"Célula '{id_celula}' está na linha {linha}, posição X={x}", fg="green"
            )
        else:
            self.resultado_busca.config(
                text=f"Célula '{id_celula}' não encontrada.", fg="red"
            )

    def remover_celula(self):
        celula_id = self.selecionado.get()
        if not celula_id:
            return

        pos = self.organizador.tabela.buscar(celula_id)
        if pos is None:
            print(f"Célula {celula_id} não encontrada.")
            return

        linha, x = pos

        celula = next((c for c in self.celulas_alocadas if c['id'] == celula_id), None)
        if celula:
            largura = celula['largura']
            # Armazena o espaço livre
            self.organizador.espacos_livres[linha].append((x, largura))
            self.organizador.espacos_livres[linha].sort()
            self.organizador.linhas[linha] -= largura

        # Remove da tabela e da lista
        self.organizador.tabela.remover(celula_id)
        self.celulas_alocadas = [c for c in self.celulas_alocadas if c['id'] != celula_id]

        menu = self.menu["menu"]
        menu.delete(0, "end")
        for celula in self.celulas_alocadas:
            menu.add_command(label=celula["id"], command=lambda v=celula["id"]: self.selecionado.set(v))
        if self.celulas_alocadas:
            self.selecionado.set(self.celulas_alocadas[0]["id"])
        else:
            self.selecionado.set("")

        self.atualizar_ocupacao()

if __name__ == "__main__":

    organizador = Organizador(LARGURA_TOTAL, ALTURA_LINHA, NUM_LINHAS)
    celulas = ler_celulas(ARQUIVO_ENTRADA)
    celulas_alocadas = alocar_celulas(organizador, celulas)
    root = tk.Tk()
    app = InterfaceTk(root, organizador, celulas_alocadas, LARGURA_TOTAL, ALTURA_LINHA, NUM_LINHAS)
    root.mainloop()
