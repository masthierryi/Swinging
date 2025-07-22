import tkinter as tk
from tkinter import font

# ===================================================================
# --- CONFIGURAÇÃO DA PARTIDA ---
# Altere os dados para o seu jogo.
# ===================================================================

NOMES_LOBBY = [
    "masthierry",    # Jogador 1
    "barteles",      # Jogador 2
    "gabrilao",      # Jogador 3
    "Teeboo",        # Jogador 4
    "vulgo pinto",   # Jogador 5
    "Tzk pj",        # Jogador 6
    "ExCaraVelho",   # Jogador 7
    "fagnin",        # Jogador 8
]

MEU_NUMERO = 1

# ===================================================================
# --- LÓGICA DO PROGRAMA (Não precisa editar abaixo) ---
# ===================================================================

class TFTScoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TFT Scout v2")
        self.root.configure(bg='#202020')

        self.posicoes = {
            1: (0, 1), 2: (0, 2), 3: (1, 2), 4: (2, 2),
            5: (2, 1), 6: (2, 0), 7: (1, 0), 8: (0, 0)
        }
        
        self.cores = {
            "possivel": "#4CAF50", "enfrentado": "#607D8B", "eu": "#2196F3",
            "eliminado": "#424242", "texto": "#FFFFFF", "eliminar_btn": "#c43737"
        }

        self.inicializar_jogo()
        self.criar_widgets()
        self.atualizar_estado_geral()

    def inicializar_jogo(self):
        self.jogadores = {i + 1: {"nome": nome, "vivo": True} for i, nome in enumerate(NOMES_LOBBY)}
        self.ultimo_oponente = None
        self.bag_de_oponentes_late_game = [] # Bag específica para o late game

    def get_jogadores_vivos(self):
        """Retorna uma lista com os números dos jogadores vivos."""
        return [n for n, d in self.jogadores.items() if d["vivo"]]

    def criar_widgets(self):
        self.botoes_principais = {}
        self.botoes_eliminar = {}
        container = tk.Frame(self.root, bg='#202020')
        container.pack(padx=10, pady=10)

        for i in range(3):
            container.grid_rowconfigure(i, weight=1, minsize=110)
            container.grid_columnconfigure(i, weight=1, minsize=120)

        bold_font = font.Font(family="Helvetica", size=10, weight="bold")
        
        for num, dados in self.jogadores.items():
            pos = self.posicoes[num]
            
            # Frame para cada "ilha" de jogador
            ilha_frame = tk.Frame(container, bg='#333333', relief=tk.RAISED, borderwidth=2)
            ilha_frame.grid(row=pos[0], column=pos[1], padx=5, pady=5, sticky="nsew")
            
            # Botão principal com o nome do jogador
            botao_principal = tk.Button(
                ilha_frame, text=dados['nome'], font=bold_font, fg=self.cores["texto"],
                wraplength=110, command=lambda n=num: self.clique_enfrentei(n)
            )
            botao_principal.pack(expand=True, fill='both', padx=5, pady=5)
            self.botoes_principais[num] = botao_principal

            # Botão 'X' para eliminar
            botao_x = tk.Button(
                ilha_frame, text="X", font=("Helvetica", 8, "bold"), bg=self.cores['eliminar_btn'],
                fg='white', command=lambda n=num: self.eliminar_jogador(n),
                relief=tk.FLAT, width=2, height=1
            )
            botao_x.place(relx=1.0, rely=0.0, anchor='ne')
            self.botoes_eliminar[num] = botao_x

    def clique_enfrentei(self, num_jogador):
        if num_jogador == MEU_NUMERO or not self.jogadores[num_jogador]["vivo"]:
            return

        self.ultimo_oponente = num_jogador
        self.atualizar_estado_geral()
        
    def eliminar_jogador(self, num_jogador):
        if not self.jogadores[num_jogador]["vivo"]:
            return
            
        self.jogadores[num_jogador]["vivo"] = False
        print(f"Jogador {self.jogadores[num_jogador]['nome']} eliminado.")
        self.atualizar_estado_geral()

    def atualizar_estado_geral(self):
        """Função central que recalcula oponentes e atualiza cores."""
        jogadores_vivos = self.get_jogadores_vivos()
        oponentes_vivos = [p for p in jogadores_vivos if p != MEU_NUMERO]
        
        possiveis_oponentes = []

        # LATE GAME: 4 ou menos jogadores vivos -> Lógica de Bag Estrita
        if len(jogadores_vivos) <= 4:
            # Se a bag está vazia ou o último oponente não está mais na bag (foi eliminado)
            if not self.bag_de_oponentes_late_game or self.ultimo_oponente not in self.bag_de_oponentes_late_game:
                self.bag_de_oponentes_late_game = [p for p in oponentes_vivos if p != self.ultimo_oponente]
                print(f"--- LATE GAME: Bag Recarregada -> {self.bag_de_oponentes_late_game}")
            
            # Se o último oponente enfrentado está na bag, remova-o
            if self.ultimo_oponente in self.bag_de_oponentes_late_game:
                 self.bag_de_oponentes_late_game.remove(self.ultimo_oponente)

            possiveis_oponentes = self.bag_de_oponentes_late_game

        # EARLY/MID GAME: Mais de 4 jogadores -> Lógica Simples
        else:
            possiveis_oponentes = [p for p in oponentes_vivos if p != self.ultimo_oponente]
            self.bag_de_oponentes_late_game = [] # Reseta a bag do late game
        
        print(f"Oponentes Possíveis: {[self.jogadores[p]['nome'] for p in possiveis_oponentes]}")
        self.atualizar_cores_botoes(possiveis_oponentes)

    def atualizar_cores_botoes(self, possiveis_oponentes):
        for num, botao in self.botoes_principais.items():
            if not self.jogadores[num]["vivo"]:
                botao.config(bg=self.cores["eliminado"], state=tk.DISABLED)
                self.botoes_eliminar[num].config(state=tk.DISABLED, relief=tk.FLAT)
            elif num == MEU_NUMERO:
                botao.config(bg=self.cores["eu"], state=tk.DISABLED)
                self.botoes_eliminar[num].config(state=tk.DISABLED, relief=tk.FLAT)
            elif num in possiveis_oponentes:
                botao.config(bg=self.cores["possivel"], state=tk.NORMAL)
            else:
                botao.config(bg=self.cores["enfrentado"], state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TFTScoutApp(root)
    root.mainloop()